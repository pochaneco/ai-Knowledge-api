# システムアーキテクチャ

Vidaysのシステム構成とアーキテクチャについて説明します。

## 🏗️ 全体アーキテクチャ

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   フロントエンド    │    │   バックエンドAPI   │    │   データベース     │
│   (Vue.js/Vite)  │◄──►│   (Flask/Python)  │◄──►│    (MySQL)     │
│   Port: 5173     │    │   Port: 5000      │    │   Port: 3306    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Inertia.js     │    │   SQLAlchemy    │    │   InnoDB Engine │
│   (SPA Bridge)   │    │   (ORM)         │    │   (Storage)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 技術スタック

### フロントエンド層
- **Vue.js 3**: リアクティブUI フレームワーク
- **Inertia.js**: SPAブリッジ（Ajax + SSR の利点）
- **Vite**: 高速ビルドツール・開発サーバー
- **Tailwind CSS**: ユーティリティファーストCSS
- **TypeScript**: 型安全性（段階的導入）

### バックエンド層
- **Flask**: 軽量Webフレームワーク
- **SQLAlchemy**: Python ORM
- **Flask-Migrate**: データベースマイグレーション
- **Flask-Login**: セッション管理
- **Authlib**: OAuth実装
- **Gunicorn**: WSGIサーバー（本番）

### データベース層
- **MySQL 8.0**: リレーショナルデータベース
- **InnoDB**: ストレージエンジン
- **utf8mb4**: 文字セット（絵文字対応）

### インフラ層
- **Docker**: コンテナ化
- **Nginx**: リバースプロキシ・静的ファイル配信
- **Let's Encrypt**: SSL証明書

## 🏢 アプリケーションアーキテクチャ

### レイヤード アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Web Routes    │  │   API Routes    │              │
│  │  (views.py)     │  │  (api/v1/*.py)  │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                     Business Layer                      │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Services      │  │   Decorators    │              │
│  │  (*_services.py)│  │  (auth/perm)    │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                      Data Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │    Models       │  │   Database      │              │
│  │  (models/*.py)  │  │   (MySQL)       │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

## 📁 モジュール構成

### Flaskアプリケーション構造

```python
app/
├── __init__.py          # アプリケーションファクトリ
├── config.py           # 設定管理
├── extensions.py       # Flask拡張機能の初期化
│
├── models/             # データモデル
│   ├── __init__.py
│   ├── user.py         # ユーザーモデル
│   ├── project.py      # プロジェクトモデル
│   ├── knowledge.py    # ナレッジモデル
│   └── search_log.py   # 検索ログモデル
│
├── api/v1/             # REST API
│   ├── __init__.py
│   ├── auth_api.py     # 認証API
│   ├── projects_api.py # プロジェクトAPI
│   └── knowledge_api.py# ナレッジAPI
│
├── auth/               # 認証機能
│   ├── __init__.py
│   ├── routes.py       # 認証ルート
│   ├── services.py     # 認証ビジネスロジック
│   └── views.py        # 認証ビュー
│
├── projects/           # プロジェクト機能
│   ├── __init__.py
│   ├── routes.py       # プロジェクトルート
│   ├── services.py     # プロジェクトビジネスロジック
│   └── views.py        # プロジェクトビュー
│
├── knowledge/          # ナレッジ機能
│   ├── services.py     # ナレッジビジネスロジック
│   └── views.py        # ナレッジビュー
│
└── utils/              # ユーティリティ
    ├── decorators.py   # カスタムデコレータ
    ├── logger.py       # ログ設定
    └── validators.py   # バリデーション
```

## 🔄 データフロー

### 典型的なリクエストフロー

```
1. ユーザーアクション (Vue.js)
         ↓
2. Inertia.jsリクエスト
         ↓
3. Flask Route Handler
         ↓
4. Service Layer (ビジネスロジック)
         ↓
5. Model Layer (データアクセス)
         ↓
6. Database (MySQL)
         ↓
7. レスポンスデータの構築
         ↓
8. JSON/Inertia レスポンス
         ↓
9. Vue.js コンポーネント更新
```

### 認証フロー

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │   Server    │    │  Database   │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ 1. Login Request │                  │
       ├─────────────────►│                  │
       │                  │ 2. Validate User│
       │                  ├─────────────────►│
       │                  │ 3. User Data    │
       │                  │◄─────────────────┤
       │                  │ 4. Create Session
       │                  │                  │
       │ 5. Session Cookie│                  │
       │◄─────────────────┤                  │
       │                  │                  │
       │ 6. API Request + │                  │
       │    Session Cookie│                  │
       ├─────────────────►│                  │
       │                  │ 7. Validate Session
       │                  │                  │
       │ 8. API Response  │                  │
       │◄─────────────────┤                  │
```

## 🗄️ データベース設計

### ERD（Entity Relationship Diagram）

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      Users      │    │  ProjectMembers │    │    Projects     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ email           │◄──►│ user_id (FK)    │◄──►│ name            │
│ password_hash   │    │ project_id (FK) │    │ description     │
│ name            │    │ role            │    │ created_at      │
│ is_active       │    │ joined_at       │    │ updated_at      │
│ created_at      │    └─────────────────┘    └─────────────────┘
│ updated_at      │              │                      │
└─────────────────┘              │                      │
         │                       │                      │
         │              ┌─────────────────┐             │
         │              │ KnowledgeBases  │             │
         │              ├─────────────────┤             │
         │              │ id (PK)         │             │
         └─────────────►│ author_id (FK)  │             │
                        │ project_id (FK) │◄────────────┘
                        │ title           │
                        │ content         │
                        │ tags            │
                        │ created_at      │
                        │ updated_at      │
                        └─────────────────┘
```

### インデックス戦略

```sql
-- ユーザー検索の最適化
CREATE INDEX idx_users_email ON users(email);

-- プロジェクトメンバー検索の最適化
CREATE INDEX idx_project_members_user_project ON project_members(user_id, project_id);

-- ナレッジ検索の最適化
CREATE INDEX idx_knowledge_project_id ON knowledge_bases(project_id);
CREATE INDEX idx_knowledge_author_id ON knowledge_bases(author_id);
CREATE FULLTEXT INDEX idx_knowledge_search ON knowledge_bases(title, content);

-- タグ検索の最適化
CREATE INDEX idx_knowledge_tags ON knowledge_bases(tags);
```

## 🔒 セキュリティアーキテクチャ

### 認証・認可

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                      │
├─────────────────────────────────────────────────────────┤
│ 1. Transport Security (HTTPS/TLS)                      │
├─────────────────────────────────────────────────────────┤
│ 2. Authentication (Session/OAuth)                      │
├─────────────────────────────────────────────────────────┤
│ 3. Authorization (Role-based Access Control)           │
├─────────────────────────────────────────────────────────┤
│ 4. Input Validation (SQLAlchemy ORM)                   │
├─────────────────────────────────────────────────────────┤
│ 5. Output Encoding (Jinja2 Auto-escape)                │
└─────────────────────────────────────────────────────────┘
```

### RBAC（Role-Based Access Control）

```python
# プロジェクトロール階層
ROLE_HIERARCHY = {
    'owner': ['admin', 'member'],
    'admin': ['member'],
    'member': []
}

# 権限マトリックス
PERMISSIONS = {
    'project': {
        'read': ['owner', 'admin', 'member'],
        'update': ['owner', 'admin'],
        'delete': ['owner'],
        'invite_member': ['owner', 'admin'],
        'remove_member': ['owner', 'admin']
    },
    'knowledge': {
        'read': ['owner', 'admin', 'member'],
        'create': ['owner', 'admin', 'member'],
        'update': ['owner', 'admin', 'member'],  # 作成者のみ
        'delete': ['owner', 'admin', 'member']   # 作成者のみ
    }
}
```

## 📈 スケーラビリティ設計

### 水平スケーリング対応

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
│                      (Nginx)                            │
└─────────────────┬───────────────────┬───────────────────┘
                  │                   │
         ┌─────────────────┐  ┌─────────────────┐
         │   App Server 1  │  │   App Server 2  │
         │   (Gunicorn)    │  │   (Gunicorn)    │
         └─────────────────┘  └─────────────────┘
                  │                   │
                  └─────────┬─────────┘
                           │
                ┌─────────────────┐
                │   Database      │
                │   (MySQL)       │
                │ + Read Replicas │
                └─────────────────┘
```

### キャッシュ戦略

```python
# Redis実装例
CACHE_CONFIG = {
    'user_sessions': 'redis://localhost:6379/0',
    'api_responses': 'redis://localhost:6379/1',
    'search_results': 'redis://localhost:6379/2'
}

# メモリキャッシュ（アプリケーションレベル）
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_project_members(project_id):
    return ProjectMember.query.filter_by(project_id=project_id).all()
```

## 🔄 CI/CD パイプライン

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          pip install -r requirements.txt
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: |
          ssh user@server 'cd /var/www/app && git pull && systemctl restart app'
```

## 📊 監視・ログ

### ログ構成

```python
# app/utils/logger.py
LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'detailed'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'app': {
            'level': 'INFO',
            'handlers': ['file', 'console']
        },
        'sqlalchemy': {
            'level': 'WARNING',
            'handlers': ['file']
        }
    }
}
```

### メトリクス収集

- **アプリケーションメトリクス**: レスポンス時間、エラー率
- **インフラメトリクス**: CPU、メモリ、ディスク使用率
- **ビジネスメトリクス**: ユーザー数、プロジェクト数、API利用統計

## 🔮 将来の拡張計画

### マイクロサービス化

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Auth Service  │    │ Project Service │    │Knowledge Service│
│   (独立DB)      │    │   (独立DB)      │    │   (独立DB)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   API Gateway   │
                    │   (Kong/Nginx)  │
                    └─────────────────┘
```

### 検索エンジン統合

```
┌─────────────────┐    ┌─────────────────┐
│   Application   │◄──►│  Elasticsearch  │
│                 │    │   (Full-text)   │
└─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│     MySQL       │    │     Logstash    │
│   (Structured)  │    │   (Data Sync)   │
└─────────────────┘    └─────────────────┘
```

## 🎯 パフォーマンス目標

- **レスポンス時間**: 95%のリクエストが200ms以内
- **可用性**: 99.9%のアップタイム
- **スループット**: 1000 req/sec
- **データベース**: クエリ実行時間の平均50ms以内
