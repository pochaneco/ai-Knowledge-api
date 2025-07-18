# AI Knowledge API

AI知識管理APIです。
プロジェクトごとに知識を管理できます。
メンバー招待機能で、プロジェクトを共有できます。


## 🚀 特徴

- **SQLAlchemy ORM**: 高レベルなデータベース操作
- **Flask-Migrate**: データベースマイグレーション機能
- **環境別設定**: ローカル/本番環境の設定切り替え
- **REST API**: ユーザーとナレッジ管理のAPI
- **Inertia.js**: モダンなSPA体験を提供するフロントエンド
- **Vue.js**: リアクティブなユーザーインターフェース
- **Tailwind CSS**: 効率的なスタイリング
- **index.cgi付き**: 共用レンタルサーバー等の制限環境での動作

## 📦 セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. フロントエンド依存関係のインストール

```bash
npm install
```

### 3. 環境設定

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

### 4. アプリケーション起動

#### 開発環境（推奨）- ルートディレクトリから

```bash
# 全ての依存関係をインストール
npm run install:all

# フロントエンドとバックエンドを同時起動
npm run dev:full

# または個別に起動
npm run dev:frontend  # フロントエンドのみ
npm run dev:backend   # バックエンドのみ
```

#### 開発環境（従来の方法）- 個別起動

```bash
# バックエンド起動（ターミナル1）
./scripts/run_app.sh local

# フロントエンド開発サーバー起動（ターミナル2）
npm run dev:frontend
```

#### Docker環境での開発

```bash
# Docker開発環境を起動（全サービス）
make docker-dev

# または個別にサービスを起動
make docker-frontend-only  # フロントエンドのみ
make docker-backend-only   # バックエンドのみ

# Docker経由でnpmコマンドを実行
make docker-npm-install           # 依存関係をインストール
make docker-npm-build            # プロダクションビルド
make docker-npm-exec cmd="test"  # 任意のnpmコマンドを実行
```

#### 本番環境

```bash
# フロントエンドビルド
npm run build

# バックエンド起動
npm run backend:prod
```

# または手動で起動
./scripts/setup_env.sh local
python app.py

# index.cgiで動作する環境ではセットアップのみで起動
# ただし、pipのインストールが必要
./scripts/install_packages.sh
./scripts/setup_env.sh production
./scripts/setup_permissions.sh
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

### バックエンド
- `app.py` - メインアプリケーション（SQLAlchemy対応）
- `app/` - アプリケーションパッケージ
  - `models/` - SQLAlchemyモデル定義
  - `api/` - REST APIエンドポイント
  - `auth/` - 認証関連
  - `projects/` - プロジェクト管理
  - `knowledge/` - ナレッジベース
  - `templates/` - Inertia.js用テンプレート
  - `static/` - 静的ファイル
- `config.py` - 環境別設定クラス
- `requirements.txt` - Python依存関係
- `migrations/` - Flask-Migrateで生成されるマイグレーションファイル

### フロントエンド
- `frontend/` - フロントエンドアプリケーション
  - `src/` - ソースファイル
    - `pages/` - Vueページコンポーネント
    - `components/` - 再利用可能なコンポーネント
    - `layouts/` - レイアウトコンポーネント
    - `utils/` - ユーティリティ関数
  - `package.json` - Node.js依存関係
  - `vite.config.js` - Vite設定
  - `tailwind.config.js` - Tailwind CSS設定

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

### 開発環境のセットアップ

#### フロントエンド + バックエンドの同時開発
```bash
# 全依存関係をインストール
make install-dev
make npm-install

# 開発サーバーを同時起動（推奨）
make dev
# これにより以下が同時起動されます:
# - Flask開発サーバー: http://localhost:5000
# - Vite開発サーバー: http://localhost:3000
```

#### 個別開発サーバー
```bash
# バックエンドのみ起動
make run-dev

# フロントエンドのみ起動
make npm-dev

# フロントエンドビルド（本番用）
make npm-build
```

### バックエンド開発
1. モデル変更: `app/models/` を編集
2. マイグレーション生成: `flask db migrate -m "説明"`
3. マイグレーション実行: `flask db upgrade`
4. API実装: `app/api/` にエンドポイント追加

### フロントエンド開発
1. ページ作成: `frontend/src/pages/` に新しい`.vue`ファイルを作成
2. コンポーネント作成: `frontend/src/components/` に再利用可能なコンポーネントを作成
3. ルート追加: Flaskビューで`render()`を使用して新しいページを表示
4. スタイル: Tailwind CSSユーティリティクラスを使用

### Inertia.js開発パターン

#### Flask側（バックエンド）
```python
from app.inertia_config import render

@auth_bp.route('/login')
def login():
    return render('auth/Login')

@project_bp.route('/')
def index():
    projects = Project.query.all()
    return render('projects/Index', {
        'projects': [p.to_dict() for p in projects]
    })
```

#### Vue側（フロントエンド）
```vue
<template>
  <div>
    <h1>{{ title }}</h1>
    <div v-for="project in projects" :key="project.id">
      {{ project.name }}
    </div>
  </div>
</template>

<script>
import { Head, Link } from '@inertiajs/vue3'

export default {
  components: { Head, Link },
  props: {
    projects: Array,
  },
}
</script>
```

### 新しいページの追加手順
1. **Flaskビューの作成**
   ```python
   @blueprint.route('/new-page')
   def new_page():
       return render('NewPage', {'data': 'example'})
   ```

2. **Vueコンポーネントの作成**
   ```bash
   touch frontend/src/pages/NewPage.vue
   ```

3. **コンポーネントの実装**
   ```vue
   <template>
     <div>
       <Head title="新しいページ" />
       <h1>新しいページ</h1>
     </div>
   </template>
   
   <script>
   import { Head } from '@inertiajs/vue3'
   
   export default {
     components: { Head },
     props: {
       data: String,
     },
   }
   </script>
   ```
    return render('Users/Index', {
        'users': [user.to_dict() for user in users]
    })
```

```vue
<!-- Vue側（フロントエンド） -->
<template>
  <div>
    <h1>ユーザー一覧</h1>
    <div v-for="user in users" :key="user.id">
      {{ user.username }}
    </div>
  </div>
</template>

<script>
export default {
  props: ['users'],
}
</script>
```

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
