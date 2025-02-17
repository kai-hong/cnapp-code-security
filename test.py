

import os
import requests
import boto3
import subprocess
import json

# 🚨 1. Secrets（敏感資訊暴露）
# ❌ 這是一個硬編碼的 AWS Secret Key，會被檢測到
AWS_ACCESS_KEY_ID = "AKIAFAKEKEY123456789"
AWS_SECRET_ACCESS_KEY = "fakeSecretKey123456789abcdefgh"
GITHUB_TOKEN = "ghp_fakeGitHubToken123456789"

# 🚨 2. IaC（基礎設施即代碼）
# ❌ Terraform 配置，使用過時的 TLS 1.0
terraform_config = """
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  metadata_options {
    http_tokens = "optional"  # ❌ 這會導致元資料洩露風險
  }
}
"""
with open("insecure.tf", "w") as f:
    f.write(terraform_config)

# 🚨 3. CI/CD Hardening（CI/CD 安全強化）
# ❌ 在 CI/CD Pipeline 中使用 TLS 1.0
subprocess.run(["curl", "--tlsv1.0", "https://example.com"], check=False)

# 🚨 4. Open Source（開源漏洞）
# ❌ 使用過時的 Python 套件，包含已知漏洞
requirements_txt = """
Django==1.11.29  # ❌ 這個版本包含已知安全漏洞
Flask==0.12.3  # ❌ 這個版本也有漏洞
"""
with open("requirements.txt", "w") as f:
    f.write(requirements_txt)

# 🚨 5. Sprawl（代碼蔓延）
# ❌ 無用的敏感憑證暴露在多個檔案
sprawl_secret = "sprawl_fake_secret_ABC123"
with open("config.json", "w") as f:
    json.dump({"api_key": sprawl_secret}, f)

# 🚨 6. 觸發 API Call，模擬風險場景
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
requests.get("https://api.github.com/user", headers=headers)

# 🚨 7. 使用 AWS SDK，測試 Secrets 掃描
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
s3 = session.resource("s3")
for bucket in s3.buckets.all():
    print(bucket.name)

print("Security test script executed.")
