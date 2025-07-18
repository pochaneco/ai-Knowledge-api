# AI Knowledge API

**SQLAlchemy対応**のFlaskベースAI知識管理APIです。ローカル開発環境と本番環境の両方でMySQL接続をサポートします。

## 🚀 特徴

- **SQLAlchemy ORM**: 高レベルなデータベース操作
- **Flask-Migrate**: データベースマイグレーション機能
- **環境別設定**: ローカル/本番環境の設定切り替え
- **REST API**: ユーザーとナレッジ管理のAPI
- **自動初期化**: サンプルデータ付きDB初期化

## 📦 セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境設定

#### ローカル開発環境
```bash
# .env.example を .env.local にコピー
cp .env.example .env.local

# .env.local を編集してローカルのMySQL接続情報を設定
vim .env.local
```

#### 本番環境
```bash
# .env.example を .env.production にコピー
cp .env.example .env.production

# .env.production を編集して本番のMySQL接続情報を設定
vim .env.production
```

### 3. アプリケーション起動

```bash
# ローカル環境で起動
./run_app.sh local

# 本番環境で起動
./run_app.sh production

# または手動で起動
./setup_env.sh local
python app.py
```

## 🎯 API エンドポイント

### 基本
- `GET /` - ホームページ（SQLAlchemy対応UI）
- `GET /test` - API動作確認
- `GET /db-test` - SQLAlchemyデータベース接続テスト
- `GET /config-info` - 現在の設定情報表示
- `GET /init-db` - データベース初期化とサンプルデータ作成

### ユーザー管理
- `GET /users` - 全ユーザー取得
- `POST /users` - ユーザー作成
  ```json
  {
    "username": "new_user",
    "email": "user@example.com"
  }
  ```

### ナレッジ管理
- `GET /knowledge` - ナレッジ一覧取得（ページネーション対応）
  - クエリパラメータ: `?page=1&per_page=10&category=Programming`
- `POST /knowledge` - ナレッジ作成
  ```json
  {
    "title": "新しいナレッジ",
    "content": "内容...",
    "category": "Programming",
    "tags": ["Python", "Flask"],
    "user_id": 1
  }
  ```

## 🗄️ データベースマイグレーション

Flask-Migrateを使用したデータベーススキーマ管理：

```bash
# マイグレーション初期化（初回のみ）
flask db init

# マイグレーションファイル生成
flask db migrate -m "Initial migration"

# マイグレーション実行
flask db upgrade

# 現在の状態確認
flask db current
```

## 🔧 環境設定ファイル

### .env.local (ローカル開発用)
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_local_password
DB_NAME=ai_knowledge_db
DB_CHARSET=utf8mb4
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_development_secret_key
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=True
```

### .env.production (本番環境用)
```env
DB_HOST=your_production_host
DB_PORT=3306
DB_USER=production_user
DB_PASSWORD=your_production_password
DB_NAME=ai_knowledge_production
DB_CHARSET=utf8mb4
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_production_secret_key
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=False
```

## 📁 ファイル構成

- `app.py` - メインアプリケーション（SQLAlchemy対応）
- `models.py` - SQLAlchemyモデル定義
- `config.py` - 環境別設定クラス
- `database.py` - レガシーデータベース接続（参考用）
- `migrate.py` - Flask-Migrate設定
- `requirements.txt` - Python依存関係（SQLAlchemy追加）
- `database_init.sql` - レガシーSQL初期化スクリプト
- `setup_env.sh` - 環境切り替えスクリプト
- `run_app.sh` - SQLAlchemy対応起動スクリプト
- `.env.example` - 環境設定テンプレート
- `migrations/` - Flask-Migrateで生成されるマイグレーションファイル

## 🧪 テスト

### テスト環境のセットアップ

#### 開発用パッケージのインストール
```bash
pip install -r requirements-dev.txt
```

### テストの実行

#### 全てのテストを実行
```bash
make test
# または
pytest
```

#### ユニットテストのみ実行
```bash
make test-unit
# または
pytest -m "not integration"
```

#### 統合テストのみ実行
```bash
make test-integration
# または
pytest -m integration
```

#### カバレッジレポート付きでテスト実行
```bash
make test-coverage
# または
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Dockerでのテスト実行

#### テスト専用環境でテスト実行
```bash
docker-compose -f docker-compose.test.yml up --build
```

#### 既存のDocker環境でテスト実行
```bash
make docker-test
# または
docker-compose exec web pytest
```

### テストファイル構成

```
tests/
├── conftest.py           # pytest設定とフィクスチャ
├── test_auth.py          # 認証関連のテスト
├── test_projects.py      # プロジェクト関連のテスト
├── test_knowledge.py     # ナレッジベース関連のテスト
├── test_models.py        # モデル関連のテスト
└── test_integration.py   # 統合テスト
```

### テストの書き方

#### 新しいテストファイルの作成
```python
# tests/test_new_feature.py
import pytest

class TestNewFeature:
    def test_new_functionality(self, authenticated_client):
        """新機能のテスト"""
        response = authenticated_client.get('/api/v1/new-endpoint')
        assert response.status_code == 200
        assert 'expected_key' in response.json
```

#### フィクスチャの使用
- `app`: テスト用Flaskアプリケーション
- `client`: テスト用HTTPクライアント
- `authenticated_client`: 認証済みクライアント
- `test_user`: テスト用ユーザー
- `test_project`: テスト用プロジェクト
- `test_knowledge_base`: テスト用ナレッジベース

### CI/CDでのテスト

GitHub Actionsが設定されており、プッシュやプルリクエスト時に自動でテストが実行されます。

```bash
# ローカルでのlint実行
make lint

# ローカルでのコードフォーマット
make format
```

## 🛠️ 開発ワークフロー

### 新機能開発
1. モデル変更: `models.py` を編集
2. マイグレーション生成: `flask db migrate -m "説明"`
3. マイグレーション実行: `flask db upgrade`
4. API実装: `app.py` にエンドポイント追加

### データベーススキーマ変更
```bash
# 1. モデルを変更
vim models.py

# 2. マイグレーション生成
flask db migrate -m "Add new column to users table"

# 3. 生成されたマイグレーションファイルを確認
cat migrations/versions/xxx_add_new_column_to_users_table.py

# 4. マイグレーション実行
flask db upgrade
```

## セキュリティ注意事項

- `.env.local` と `.env.production` は `.gitignore` に含まれているため、Gitリポジトリにコミットされません
- 本番環境では強力なパスワードとシークレットキーを使用してください
- データベースユーザーには必要最小限の権限のみを付与してください

## トラブルシューティング

### データベース接続エラー
1. MySQL サービスが起動しているか確認
2. 接続情報（ホスト、ポート、ユーザー名、パスワード）が正しいか確認
3. データベースが存在するか確認

### 依存関係エラー
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
