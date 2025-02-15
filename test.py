import os
import requests
import boto3  # Open Source library example (AWS SDK) 1

import requests
import random
import string
import qrcode
import os
import base64
import xlsxwriter

# ==============================
# 🚨 [Secrets] 硬編碼 API 金鑰
# ==============================
AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7SECRETKEYEXAMPLE"  # ❌ 不應該硬編碼
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"  # ❌ GitHub API Token
DATABASE_PASSWORD = "P@ssw0rd!"  # ❌ 資料庫密碼

# 這些密碼應該存放在環境變數或密鑰管理服務，而不是直接寫在程式碼中：
# os.getenv("AWS_SECRET_ACCESS_KEY")

# ==============================
# 🚨 [IaC] 錯誤的基礎設施代碼
# ==============================
insecure_terraform_config = """
resource "aws_security_group" "bad_sg" {
  name        = "insecure-sg"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # ❌ 開放所有 IP，存在重大安全風險
  }
}
"""
# 建議：應該限制 IP 來源，例如 ["192.168.1.0/24"]

# ==============================
# 🚨 [CI/CD Hardening] 不安全的 GitHub Actions
# ==============================
insecure_github_action = """
name: Deploy to Production
on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Deploy to Server
        run: |
          ssh root@0.0.0.0 "deploy.sh"  # ❌ 直接使用 root 使用者，沒有 Multi-Factor Authentication
"""
# 建議：使用 OpenID Connect (OIDC) 或安全的 SSH Key，而非 root 密碼登入

# ==============================
# 🚨 [Open Source] 易受攻擊的依賴
# ==============================
# 使用已知存在漏洞的 Flask 版本（CVE-2023-XXXX）
insecure_requirements_txt = """
flask==1.1.1  # ❌ 這個版本的 Flask 存在已知漏洞
requests==2.19.1  # ❌ 這個版本的 requests 存在安全性問題
"""

# 建議：應該更新到 Flask 2.0+ 和 requests 最新版本，並使用 Snyk 或 Dependabot 監控套件更新。

# ==============================
# 🚨 [Sprawl] 未使用的敏感資訊
# ==============================
UNUSED_API_KEY = "sk_test_51KQwp9J7q1234567890abcdefg"  # ❌ Stripe 測試 API Key，未使用但仍然存在
EXPIRED_PASSWORD = "OldPassword123!"  # ❌ 舊密碼仍存留在代碼中

# 建議：刪除未使用的憑證，並使用 Git 秘密掃描工具，例如 GitGuardian、Spectral。

# ==============================
# 🎯 測試執行 API 請求（會使用硬編碼的憑證）
# ==============================
def make_request():
    url = "https://api.example.com/data"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"  # ❌ 使用硬編碼 Token
    }
    response = requests.get(url, headers=headers)
    print(response.json())

if __name__ == "__main__":
    make_request()


# 定义 API 请求 URL 和站点 ID
url = "https://api.mist.com/api/v1/sites/{site_id}/psks"
site_id = "6f80f028-5ce1-49f6-adfc-ba0ac4b04ff4"
api_token = "8BV1nH6vq2mfzmgTzkWr9PUekMxTxjR6kE4UlTm94qbdSaZ6EvLvWFWJDISrrxeOchUnceavvb8Z8PidtiVJZvuEuVgjv"  # 替换为您的实际 API Token

# 定義要生成的 PSK 數量
psk_count = 5

# WLAN 資訊
wlan_ssid = "Juniper Networks"

# 建立一個空的列表來保存產生的 PSK 資料
psk_data = []

# 循環生成 PSK
for i in range(psk_count):
    # 生成隨機的 passphrase
    passphrase = ''.join(random.choices(string.digits, k=8))
    # 複雜密碼 passphrase = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    # 構建請求有效載荷
    payload = {
        "usage": "single",
        "name": f"PSK{i+1}",
        "ssid": wlan_ssid,
        "passphrase": passphrase
    }

    # 設置請求標頭，包括 API Token 和 Content-Type
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }

    # 發送 POST 請求
    response = requests.post(url.format(site_id=site_id), json=payload, headers=headers)

    # 檢查響應狀態碼
    if response.status_code == 200:
        print(f"PSK{i+1} 添加成功")
        # 將 PSK 資料添加到列表中
        psk_data.append({"PSK": f"PSK{i+1}", "Passphrase": passphrase})
    else:
        print(f"PSK{i+1} 添加失敗")

# 建立 Excel 工作簿和工作表
workbook = xlsxwriter.Workbook("psk_data.xlsx")
worksheet = workbook.add_worksheet()

# 設定標題列的格式
title_format = workbook.add_format({"bold": True})

# 寫入標題列
worksheet.write(0, 0, "SSID", title_format)
worksheet.write(0, 1, "PSK", title_format)
worksheet.write(0, 2, "Passphrase", title_format)
worksheet.write(0, 3, "QR Code", title_format)

# 生成 QR 碼並寫入 XLSX
for i, psk in enumerate(psk_data, start=1):
    row = i

    # 設定所有資料的統一行高
    worksheet.set_default_row(87)

    # 設定所有資料的統一列寬
    worksheet.set_column(0, worksheet.dim_colmax, 20)

    # 寫入 PSK 資料到 XLSX
    worksheet.write(row, 0, wlan_ssid)
    worksheet.write(row, 1, psk["PSK"])
    worksheet.write(row, 2, psk["Passphrase"])

    # 生成 QR 碼並插入到 XLSX
    qr_code = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_code.add_data(f"WIFI:T:WPA;S:{wlan_ssid};P:{psk['Passphrase']};;")
    qr_code.make(fit=True)

    image_path = f"qr_code_{psk['PSK']}.png"
    qr_code_image = qr_code.make_image(fill_color="black", back_color="white")
    qr_code_image.save(image_path)

    worksheet.insert_image(row, 3, image_path, {"x_scale": 0.3, "y_scale": 0.3})

    # 調整欄位寬度
    # worksheet.set_column(2, 2, 20)

    # 調整第一行的高度為 1，達到隱藏的效果
    worksheet.set_row(0, 20)
    

# 關閉工作簿
workbook.close()

