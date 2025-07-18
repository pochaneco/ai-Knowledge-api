# Docker Compose 使用方法

## 前提条件
- Docker
- Docker Compose

## セットアップと起動

1. **環境変数ファイルの準備**
   ```bash
   # Docker開発用設定をコピー
   cp .env.docker .env.local
   
   # または .env.example から手動で設定
   cp .env.example .env.local
   # .env.local を編集して適切な値を設定
   ```

2. **Docker Composeでサービスを起動**
   ```bash
   # バックグラウンドで起動
   docker-compose up -d
   
   # ログを確認しながら起動
   docker-compose up
   ```

3. **マイグレーションの実行**
   ```bash
   # コンテナ内でマイグレーション初期化（初回のみ）
   docker-compose exec web flask db init
   
   # マイグレーション生成
   docker-compose exec web flask db migrate -m "Initial migration"
   
   # マイグレーション適用
   docker-compose exec web flask db upgrade
   ```

## サービスへのアクセス

- **Flask API**: http://localhost:5000
- **phpMyAdmin**: http://localhost:8080
  - サーバー: db
  - ユーザー名: app_user
  - パスワード: app_password

## 管理コマンド

```bash
# サービス停止
docker-compose down

# サービス停止とボリューム削除（データベースデータも削除）
docker-compose down -v

# ログ確認
docker-compose logs -f web

# コンテナ内でコマンド実行
docker-compose exec web python migrate.py

# データベースコンテナに接続
docker-compose exec db mysql -u app_user -p ai_knowledge_db
```

## 開発時のヒント

- コードの変更は自動的にコンテナに反映されます（ボリュームマウント済み）
- データベースデータは永続化されます（mysql_dataボリューム）
- 本番環境では docker-compose.prod.yml を別途作成することを推奨します
