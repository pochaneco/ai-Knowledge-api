# Docker環境セットアップガイド

Docker Composeを使用した開発環境のセットアップ方法です。

## 📋 前提条件

- Docker Desktop
- Docker Compose (通常Docker Desktopに含まれる)
- Git

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/pochaneco/vidays.git
cd vidays
```

### 2. 環境変数の設定

```bash
# Docker用環境変数ファイルをコピー（参考用）
cp .env.docker.example .env.docker.local

# または基本テンプレートから作成
cp .env.example .env

# 必要に応じて .env ファイルを編集
vim .env
```

**環境ファイルの説明:**
- `.env.example`: 基本的なテンプレート（標準ポート番号）
- `.env.docker.example`: Docker環境に最適化されたテンプレート
- `.env`: 実際に使用する設定ファイル（Git管理対象外）

**重要な設定項目:**
- `VITE_PORT`: フロントエンドのポート番号（デフォルト: 5173）
- `WEB_API_PORT`: バックエンドAPIのポート番号（デフォルト: 5000）
- `DB_FORWARD_PORT`: データベースのポート番号（デフォルト: 3306）

### 3. Dockerコンテナの起動

#### 開発モード（推奨）
```bash
# 開発環境の起動（フロントエンド分離、phpMyAdmin、MailHog含む）
docker-compose --profile dev up -d

# ログを確認する場合
docker-compose --profile dev up
```

#### 本番モード
```bash
# 本番環境の起動（バックエンドのみ）
docker-compose up -d

# ログを確認する場合
#### 開発モード
```bash
# 開発モードで起動（フロントエンド開発サーバー、phpMyAdmin、MailHog含む）
docker-compose --profile dev up -d

# またはMakefileを使用
make docker-dev

# 本番モードで起動（最小構成）
docker-compose up -d
# または
make docker-up
```

#### テストモード
```bash
# 【推奨】ローカル環境でのテスト実行（高速、SQLite使用）
pytest
# または
make test

# Docker環境でのテスト実行（CI/CD用）
make test-docker

# カバレッジ付きでテスト実行
make test-coverage

# Docker環境でのカバレッジ付きテスト実行
make test-coverage-docker

# MySQL統合テスト（Docker Compose使用）
make docker-test-mysql
```

#### Makefileコマンド一覧
```bash
# 全コマンドの確認
make help

# セットアップ
make setup-docker    # Docker環境のセットアップ
make setup-local     # ローカル環境のセットアップ

# 開発
make dev             # ローカル開発サーバー起動
make dev-docker      # Docker開発サーバー起動
make dev-logs        # 開発サーバーログ表示

# テスト
make test            # ローカルテスト（高速）
make test-docker     # Dockerテスト（CI/CD）
make test-coverage   # カバレッジレポート
```

### 4. データベースの初期化

```bash
# データベースマイグレーションの実行
docker-compose exec web flask db upgrade

# 初期データの投入（オプション）
curl http://localhost:5000/init-db
```

## 🌐 アクセス方法

### 開発モード使用時
- **メインアプリケーション**: http://localhost:5000
- **フロントエンド開発サーバー**: http://localhost:5173
- **phpMyAdmin**: http://localhost:8080
- **MailHog**: http://localhost:8025

### 本番モード使用時
- **メインアプリケーション**: http://localhost:5000

## 🛠️ 開発コマンド

### コンテナの操作

```bash
# 開発モードでコンテナの停止
make docker-down

# コンテナの状態確認
make status

# ログの確認
make logs                    # 全コンテナのログ
make dev-logs               # 開発サーバーのログ
docker-compose logs web     # 特定コンテナのログ

# コンテナの再起動
docker-compose --profile dev restart

# 完全な再構築
make docker-down
make docker-build
make docker-dev
```

### データベース操作

```bash
# マイグレーションファイルの生成
make migrate message="説明"

# マイグレーションの適用
make upgrade-db

# データベースシェルに接続
make db-shell

# または直接接続
docker-compose exec db mysql -u app_user -p ai_knowledge_db
```

### テスト実行

#### ローカル環境でのテスト（推奨）
```bash
# 高速テスト実行（SQLiteインメモリ使用）
pytest

# 詳細出力付きテスト
pytest -v

# カバレッジレポート付きテスト
pytest --cov=app --cov-report=term-missing --cov-report=html

# 特定のテストファイルのみ実行
pytest tests/test_auth.py -v
```

#### Docker環境でのテスト
```bash
# 基本的なDocker内テスト実行（CI/CD推奨）
docker build -t vidays-test . && docker run --rm -v $(pwd):/app -w /app vidays-test sh -c "PYTHONPATH=/app pytest -v"

# カバレッジ付きDocker内テスト
docker build -t vidays-test . && docker run --rm -v $(pwd):/app -w /app vidays-test sh -c "PYTHONPATH=/app pytest -v --cov=app --cov-report=term-missing --cov-report=html"

# 既存webコンテナでテスト実行
docker-compose up -d web
docker-compose exec web sh -c "PYTHONPATH=/app pytest -v"
```

#### MySQL統合テスト
```bash
# MySQL統合テスト（実際のDBを使用）
docker-compose up -d db
docker-compose --profile test run --rm test

# テストDBの確認
docker-compose exec db mysql -u root -proot_password -e "SHOW DATABASES;"
```

#### テスト環境の切り替え
```bash
# SQLiteテスト（デフォルト）
pytest

# MySQLテスト（Docker）
USE_MYSQL_FOR_TESTING=true pytest
```

#### パフォーマンス比較
| 実行環境 | 実行時間 | データベース | 用途 |
|----------|----------|--------------|------|
| ローカル | ~3秒 | SQLite | 日常開発 |
| Docker | ~16秒 | SQLite | CI/CD |
| Docker+MySQL | ~20秒+ | MySQL | 統合テスト |

### デバッグ

```bash
# コンテナ内に入る
docker-compose exec web bash
docker-compose exec frontend bash  # 開発モード時のみ

# Pythonシェルの起動
docker-compose exec web python
```

## 🔧 設定のカスタマイズ

### 開発/本番モードの切り替え

`.env`ファイルで以下の値を変更：

```env
# 開発モード
FLASK_ENV=development
NODE_ENV=development

# 本番モード
FLASK_ENV=production
NODE_ENV=production
```

### ポート番号の変更

`.env`ファイルで以下の値を変更：

```env
# フロントエンドポート
VITE_PORT=5173

# バックエンドAPIポート
WEB_API_PORT=5000

# データベースポート
DB_FORWARD_PORT=3306
```

### 開発用メール設定

MailHogを使用して開発環境でメール送信をテスト：

```env
MAIL_SERVER=mailhog
MAIL_PORT=1025
MAIL_USE_TLS=false
```

## 📝 トラブルシューティング

### ポート競合エラー

```bash
# 使用中のポートを確認
netstat -tlnp | grep :5000

# 別のポート番号に変更するか、使用中のプロセスを停止
```

### データベース接続エラー

```bash
# データベースコンテナの状態確認
docker-compose ps db

# データベースログの確認
docker-compose logs db
```

### フロントエンドビルドエラー

```bash
# node_modulesの再インストール
docker-compose -f docker-compose.dev.yml exec frontend rm -rf node_modules
docker-compose -f docker-compose.dev.yml exec frontend npm install
```

## 🎯 本番環境への移行

本番環境では開発用サービスを除外して起動：

```bash
# 本番用の環境変数設定
cp .env.example .env.production
# .env.production を本番用に設定

# 本番用の起動（開発用サービスなし）
docker-compose up -d
```

### 本番用設定例

```env
# .env.production
FLASK_ENV=production
NODE_ENV=production
FLASK_DEBUG=False
SQLALCHEMY_ECHO=False
SECRET_KEY=your_very_secure_secret_key_here
```
