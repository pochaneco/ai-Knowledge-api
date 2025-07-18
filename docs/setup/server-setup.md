# サーバー環境セットアップガイド

本番サーバーまたは共用レンタルサーバーでのデプロイ方法です。

## 📋 対応環境

### 推奨サーバー環境
- **VPS/専用サーバー**: Ubuntu 20.04+, CentOS 8+
- **共用レンタルサーバー**: CGI対応、Python 3.8+
- **クラウド**: AWS EC2, Google Cloud Compute Engine, Azure VM

### 必要な要件
- Python 3.8以上
- MySQL 8.0または互換データベース
- Web サーバー（Apache/Nginx）
- HTTPS対応（推奨）

## 🚀 VPS/専用サーバーでのセットアップ

### 1. サーバーの基本設定

```bash
# システムのアップデート
sudo apt update && sudo apt upgrade -y

# 必要なパッケージのインストール
sudo apt install -y python3 python3-pip python3-venv mysql-server nginx git
```

### 2. MySQLの設定

```bash
# MySQLの初期設定
sudo mysql_secure_installation

# データベースとユーザーの作成
sudo mysql -u root -p
```

```sql
CREATE DATABASE ai_knowledge_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON ai_knowledge_db.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. アプリケーションのデプロイ

```bash
# デプロイ用ディレクトリの作成
sudo mkdir -p /var/www/ai-knowledge-api
sudo chown $USER:www-data /var/www/ai-knowledge-api

# アプリケーションのクローン
cd /var/www/ai-knowledge-api
git clone https://github.com/pochaneco/ai-Knowledge-api.git .

# Python仮想環境の作成
python3 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
pip install gunicorn  # WSGIサーバー
```

### 4. 本番用環境設定

```bash
# 本番用環境変数ファイルの作成
cp .env.example .env.production
```

`.env.production`の編集：

```env
# 本番用データベース設定
DB_HOST=localhost
DB_PORT=3306
DB_USER=app_user
DB_PASSWORD=secure_password_here
DB_NAME=ai_knowledge_db

# 本番用Flask設定
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here

# セキュリティ設定
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=False

# 本番用メール設定
MAIL_SERVER=smtp.your-domain.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=noreply@your-domain.com
MAIL_PASSWORD=your_mail_password

# Google OAuth設定（本番用）
GOOGLE_CLIENT_ID=your_production_google_client_id
GOOGLE_CLIENT_SECRET=your_production_google_client_secret
```

### 5. データベースマイグレーション

```bash
# 環境変数の設定
export $(cat .env.production | xargs)

# マイグレーションの実行
flask db upgrade
```

### 6. フロントエンドビルド

```bash
# Node.jsのインストール（必要な場合）
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# フロントエンド依存関係のインストール
npm install

# 本番用ビルド
npm run build
```

### 7. Gunicornの設定

`gunicorn.conf.py`ファイルの作成：

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
preload_app = True
timeout = 30
keepalive = 2
user = "www-data"
group = "www-data"
```

### 8. Systemdサービスの作成

`/etc/systemd/system/ai-knowledge-api.service`：

```ini
[Unit]
Description=AI Knowledge API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-knowledge-api
Environment="PATH=/var/www/ai-knowledge-api/venv/bin"
EnvironmentFile=/var/www/ai-knowledge-api/.env.production
ExecStart=/var/www/ai-knowledge-api/venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# サービスの有効化と起動
sudo systemctl daemon-reload
sudo systemctl enable ai-knowledge-api
sudo systemctl start ai-knowledge-api
```

### 9. Nginxの設定

`/etc/nginx/sites-available/ai-knowledge-api`：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # HTTPSへのリダイレクト
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL証明書の設定
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # セキュリティ設定
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # 静的ファイルの配信
    location /static/ {
        alias /var/www/ai-knowledge-api/app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # APIリクエストのプロキシ
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# サイトの有効化
sudo ln -s /etc/nginx/sites-available/ai-knowledge-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🏠 共用レンタルサーバーでのセットアップ

### 1. ファイルのアップロード

```bash
# ローカルでファイルを準備
git clone https://github.com/pochaneco/ai-Knowledge-api.git
cd ai-Knowledge-api

# 本番用ビルド
npm install
npm run build

# ファイルをサーバーにアップロード（FTP/SFTP）
```

### 2. CGI設定

`.htaccess`ファイルの作成：

```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.cgi/$1 [QSA,L]

# Python CGIの設定
AddHandler cgi-script .cgi
Options +ExecCGI
```

### 3. CGIスクリプトの設定

`index.cgi`ファイル（既存）の権限設定：

```bash
chmod 755 index.cgi
```

### 4. 環境設定

共用サーバー用の環境変数設定を`app/config.py`に直接記述またはサーバーの環境変数機能を使用。

## 🔒 セキュリティ設定

### 1. ファイアウォール設定

```bash
# UFWを使用した基本設定
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 2. SSL証明書の設定

```bash
# Let's Encryptを使用
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. セキュリティヘッダー

Nginxに追加設定：

```nginx
# セキュリティヘッダー
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self'" always;
```

## 🔄 本番運用

### バックアップスクリプト

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u app_user -p ai_knowledge_db > backup_${DATE}.sql
tar -czf app_backup_${DATE}.tar.gz /var/www/ai-knowledge-api --exclude=venv --exclude=node_modules
```

### ログ監視

```bash
# アプリケーションログの確認
sudo journalctl -u ai-knowledge-api -f

# Nginxログの確認
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### アップデート手順

```bash
# アプリケーションの停止
sudo systemctl stop ai-knowledge-api

# コードの更新
git pull origin main

# 依存関係の更新
source venv/bin/activate
pip install -r requirements.txt

# データベースマイグレーション
flask db upgrade

# フロントエンドビルド
npm install
npm run build

# アプリケーションの再起動
sudo systemctl start ai-knowledge-api
```

## 📊 監視とメンテナンス

### パフォーマンス監視

- **サーバーリソース**: htop, iostat
- **アプリケーション**: New Relic, Datadog
- **データベース**: MySQL Workbench, phpMyAdmin

### 定期メンテナンス

- ログファイルのローテーション
- データベースの最適化
- セキュリティアップデート
- SSL証明書の更新

## 📝 トラブルシューティング

### よくある問題

1. **502 Bad Gateway**: Gunicornサービスの状態確認
2. **データベース接続エラー**: 認証情報とファイアウォール設定の確認
3. **静的ファイル404**: Nginxの設定とファイルパーミッションの確認
4. **SSL証明書エラー**: 証明書の有効期限と設定の確認
