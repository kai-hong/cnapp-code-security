import os
import requests
import boto3  # Open Source library example (AWS SDK)

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
