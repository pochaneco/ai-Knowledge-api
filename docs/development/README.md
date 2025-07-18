# 開発ガイド

AI Knowledge APIの開発に参加するための包括的なガイドです。

## 📁 プロジェクト構造

```
ai-Knowledge-api/
├── app/                    # Flaskアプリケーション
│   ├── __init__.py        # アプリケーションファクトリ
│   ├── config.py          # 設定管理
│   ├── extensions.py      # Flask拡張機能の初期化
│   ├── api/               # REST API
│   │   └── v1/           # APIバージョン1
│   ├── auth/             # 認証機能
│   ├── models/           # データベースモデル
│   ├── projects/         # プロジェクト管理
│   ├── knowledge/        # 知識管理
│   ├── static/           # 静的ファイル
│   ├── templates/        # Jinja2テンプレート
│   └── utils/            # ユーティリティ
├── frontend/              # Vue.js フロントエンド
│   └── src/
│       ├── components/   # Vueコンポーネント
│       ├── pages/        # ページコンポーネント
│       ├── layouts/      # レイアウトコンポーネント
│       └── utils/        # フロントエンドユーティリティ
├── tests/                # テストファイル
├── docs/                 # ドキュメント
├── scripts/              # 運用スクリプト
└── docker/               # Docker設定
```

## 🛠️ 開発フロー

### 1. 新機能の開発

```bash
# 新しいブランチを作成
git checkout -b feature/new-feature

# 開発環境の起動
# Docker環境の場合:
docker-compose -f docker-compose.dev.yml up -d

# venv環境の場合:
source .venv/bin/activate
export $(cat .env.local | xargs)
python app.py &
npm run dev &
```

### 2. テスト駆動開発

```bash
# 【推奨】ローカルでの高速テスト（SQLite、日常開発用）
pytest

# 詳細出力付きテスト
pytest -v

# カバレッジレポート生成
pytest --cov=app --cov-report=html

# Docker環境でのテスト（CI/CD用）
docker build -t ai-knowledge-test . && docker run --rm -v $(pwd):/app -w /app ai-knowledge-test sh -c "PYTHONPATH=/app pytest -v"

# MySQL統合テスト
docker-compose --profile test run --rm test

# テストファイルの作成
touch tests/test_new_feature.py

# 特定テストの実行
pytest tests/test_new_feature.py -v
```

#### テスト戦略
- **日常開発**: ローカル環境（SQLite）で高速テスト
- **CI/CD**: Docker環境（SQLite）で再現性確保
- **統合テスト**: MySQL環境で本番同等テスト
- **デバッグ**: 特定テストのみ実行で効率化

### 3. コード品質チェック

```bash
# コードフォーマット
black app/ tests/

# リンター
flake8 app/ tests/

# 型チェック（mypy使用時）
mypy app/
```

## 🗄️ データベース開発

### マイグレーション

```bash
# マイグレーションファイルの生成
flask db migrate -m "Add new table"

# マイグレーションの適用
flask db upgrade

# 前のバージョンにロールバック
flask db downgrade
```

### モデルの作成

```python
# app/models/example.py
from app.extensions import db
from datetime import datetime

class Example(db.Model):
    __tablename__ = 'examples'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }
```

## 🎨 フロントエンド開発

### コンポーネントの作成

```vue
<!-- frontend/src/components/ExampleComponent.vue -->
<template>
  <div class="example-component">
    <h2>{{ title }}</h2>
    <p>{{ description }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: String,
  description: String
})
</script>

<style scoped>
.example-component {
  @apply p-4 bg-white rounded-lg shadow;
}
</style>
```

### ページの作成

```vue
<!-- frontend/src/pages/Example.vue -->
<template>
  <Layout>
    <Head title="Example Page" />
    <div class="container mx-auto px-4 py-8">
      <ExampleComponent 
        :title="pageTitle" 
        :description="pageDescription" 
      />
    </div>
  </Layout>
</template>

<script setup>
import { Head } from '@inertiajs/vue3'
import Layout from '@/layouts/AppLayout.vue'
import ExampleComponent from '@/components/ExampleComponent.vue'

const pageTitle = 'Example Page'
const pageDescription = 'This is an example page.'
</script>
```

## 📡 API開発

### エンドポイントの作成

```python
# app/api/v1/example_api.py
from flask import Blueprint, request, jsonify
from app.models.example import Example
from app.extensions import db

bp = Blueprint('example_api', __name__)

@bp.route('/examples', methods=['GET'])
def get_examples():
    examples = Example.query.all()
    return jsonify([example.to_dict() for example in examples])

@bp.route('/examples', methods=['POST'])
def create_example():
    data = request.get_json()
    example = Example(name=data['name'])
    db.session.add(example)
    db.session.commit()
    return jsonify(example.to_dict()), 201
```

### APIのテスト

```python
# tests/test_example_api.py
def test_get_examples(client):
    response = client.get('/api/v1/examples')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_example(client):
    data = {'name': 'Test Example'}
    response = client.post('/api/v1/examples', json=data)
    assert response.status_code == 201
    assert response.json['name'] == 'Test Example'
```

## 🔐 認証・認可

### カスタムデコレータ

```python
# app/utils/decorators.py
from functools import wraps
from flask import jsonify
from flask_login import current_user

def require_project_permission(permission_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            project_id = kwargs.get('project_id')
            if not current_user.has_project_permission(project_id, permission_level):
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### 使用例

```python
@bp.route('/projects/<int:project_id>/knowledge', methods=['POST'])
@login_required
@require_project_permission('member')
def create_knowledge(project_id):
    # 知識の作成処理
    pass
```

## 🧪 テスト

### テストの構造

```python
# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
```

### テストの種類

1. **ユニットテスト**: 個別関数・メソッドのテスト
2. **統合テスト**: 複数コンポーネント間のテスト
3. **エンドツーエンドテスト**: ユーザーシナリオのテスト

## 📦 パッケージ管理

### Python依存関係

```bash
# 新しいパッケージのインストール
pip install package_name

# requirements.txtの更新
pip freeze > requirements.txt

# 開発用パッケージ
pip install package_name
# requirements-dev.txtに手動で追加
```

### Node.js依存関係

```bash
# 新しいパッケージのインストール
npm install package_name

# 開発用パッケージ
npm install --save-dev package_name
```

## 🚀 デプロイ

### ステージング環境

```bash
# ステージング用ブランチの作成
git checkout -b staging

# ステージング環境への自動デプロイ（CI/CD設定後）
git push origin staging
```

### 本番環境

```bash
# 本番用リリースタグの作成
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## 🔧 設定管理

### 環境ファイルの構成

```
.env.example          # 基本テンプレート（Git管理）
.env.docker.example   # Docker用テンプレート（Git管理）
.env                  # 実際の設定ファイル（Git管理対象外）
.env.local           # ローカル開発用（Git管理対象外）
.env.production      # 本番環境用（Git管理対象外）
.env.docker.local    # Docker個人設定用（Git管理対象外）
```

### 環境別設定

```python
# app/config.py
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
```

### 設定ファイルの使い分け

- **Docker開発**: `.env.docker.example` → `.env` にコピーして使用
- **ローカル開発**: `.env.example` → `.env.local` にコピーして使用
- **本番環境**: `.env.example` → `.env.production` にコピーして使用

## 📝 コーディング規約

### Python

- **PEP 8**準拠
- **Black**を使用したコードフォーマット
- **型ヒント**の使用を推奨
- **Docstring**は Google スタイル

### JavaScript/Vue.js

- **ESLint**の設定に従う
- **Prettier**を使用したコードフォーマット
- **Vue 3 Composition API**を使用
- **TypeScript**の導入を検討

### データベース

- **マイグレーション**ファイルは必ずレビュー
- **インデックス**の追加は慎重に
- **外部キー制約**を適切に設定

## 🎯 パフォーマンス

### データベース最適化

```python
# N+1問題の回避
projects = Project.query.options(
    db.joinedload(Project.members),
    db.joinedload(Project.knowledge_bases)
).all()

# ページネーション
projects = Project.query.paginate(
    page=page, per_page=20, error_out=False
)
```

### フロントエンド最適化

```javascript
// 遅延読み込み
const LazyComponent = defineAsyncComponent(() =>
  import('./components/HeavyComponent.vue')
)

// メモ化
const expensiveValue = computed(() => {
  return heavyCalculation(props.data)
})
```

## 🐛 デバッグ

### バックエンドデバッグ

```python
# ログの追加
import logging
logger = logging.getLogger(__name__)
logger.info(f"Processing request for user: {current_user.id}")

# デバッガーの使用
import pdb; pdb.set_trace()
```

### フロントエンドデバッグ

```javascript
// Vue Devtools の使用
console.log('Debug data:', reactive_data)

// ブレークポイントの設定
debugger;
```

## 📋 チェックリスト

### 機能開発完了前

- [ ] ユニットテストの作成
- [ ] 統合テストの作成
- [ ] ドキュメントの更新
- [ ] セキュリティチェック
- [ ] パフォーマンステスト
- [ ] コードレビューの完了

### デプロイ前

- [ ] 全テストの成功
- [ ] マイグレーションの確認
- [ ] 環境変数の設定確認
- [ ] セキュリティ設定の確認
- [ ] バックアップの実行
