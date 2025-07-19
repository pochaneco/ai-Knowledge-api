# Vidays プロジェクト構造ドキュメント

このドキュメントでは、Vidaysプロジェクトの新しいディレクトリ構造と各コンポーネントの役割について説明します。

## 更新内容

### 新しい構造の利点

1. **モジュール化**: 機能ごとにディレクトリを分割し、保守性を向上
2. **拡張性**: 新機能の追加が容易
3. **テスタビリティ**: テストコードの組織化
4. **ベストプラクティス**: Flaskのアプリケーションファクトリパターンを採用

### 主要な変更点

- `app.py` → `app/__init__.py` (アプリケーションファクトリ)
- `models.py` → `app/models/` (モデル分割)
- 機能別Blueprintの分割
- API v1の独立した構造
- ユーティリティ関数の分離
- テストファイルの構造化

## ディレクトリ構造

```
vidays/
├── app/                          # メインアプリケーション
│   ├── __init__.py              # アプリケーションファクトリ
│   ├── config.py                # 設定ファイル
│   ├── extensions.py            # Flask拡張機能
│   │
│   ├── models/                  # データベースモデル
│   │   ├── __init__.py
│   │   ├── user.py             # ユーザーモデル
│   │   ├── project.py          # プロジェクトモデル
│   │   ├── knowledge.py        # ナレッジベースモデル
│   │   └── search_log.py       # 検索ログモデル
│   │
│   ├── auth/                    # 認証関連
│   │   ├── __init__.py
│   │   ├── routes.py           # 認証APIルート
│   │   ├── views.py            # 認証Webビュー
│   │   └── services.py         # 認証サービス
│   │
│   ├── projects/                # プロジェクト管理
│   │   ├── __init__.py
│   │   ├── routes.py           # プロジェクトAPIルート
│   │   ├── views.py            # プロジェクトWebビュー
│   │   └── services.py         # プロジェクトサービス
│   │
│   ├── knowledge/               # ナレッジベース管理
│   │   ├── __init__.py
│   │   ├── views.py            # ナレッジベースWebビュー
│   │   └── services.py         # ナレッジベースサービス
│   │
│   ├── main/                    # メインページ
│   │   ├── __init__.py
│   │   └── views.py            # ホームページなど
│   │
│   ├── api/                     # API v1
│   │   ├── __init__.py
│   │   └── v1/                 # APIバージョン1
│   │       ├── __init__.py
│   │       ├── auth_api.py     # 認証API
│   │       ├── projects_api.py # プロジェクトAPI
│   │       └── knowledge_api.py# ナレッジベースAPI
│   │
│   ├── email/                   # メール機能
│   │   ├── __init__.py
│   │   └── services.py         # メールサービス
│   │
│   ├── utils/                   # ユーティリティ
│   │   ├── __init__.py
│   │   ├── decorators.py       # デコレータ
│   │   ├── validators.py       # バリデータ
│   │   └── logger.py           # ロガー設定
│   │
│   ├── templates/               # Jinjaテンプレート
│   │   ├── base.html           # ベーステンプレート
│   │   ├── index.html          # ホームページ
│   │   ├── auth/               # 認証関連テンプレート
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── projects/           # プロジェクト関連テンプレート
│   │   │   └── index.html
│   │   └── knowledge/          # ナレッジベース関連テンプレート
│   │       └── index.html
│   │
│   └── static/                  # 静的ファイル
│       ├── css/
│       │   └── main.css        # メインスタイルシート
│       ├── js/
│       │   └── main.js         # メインJavaScript
│       └── img/                # 画像ファイル
│
├── tests/                       # テストファイル
│   ├── conftest.py             # テスト設定
│   ├── test_auth.py            # 認証テスト
│   └── test_projects.py        # プロジェクトテスト
│
├── scripts/                     # 運用スクリプト
│   ├── migrate.py              # マイグレーション
│   ├── setup_env.sh            # 環境設定
│   ├── run_app.sh              # アプリ起動
│   ├── install_packages.sh     # パッケージインストール
│   └── setup_permissions.sh    # 権限設定
│
├── docker/                      # Docker関連
│   ├── Dockerfile              # Dockerイメージ
│   ├── docker-compose.yml      # Docker Compose設定
│   └── mysql/
│       └── init.sql            # MySQL初期化
│
├── app.py                       # アプリケーションエントリーポイント
├── config.py                    # 旧設定ファイル（退避予定）
├── requirements.txt             # Python依存関係
├── .env.example                 # 環境変数例
├── .gitignore                   # Git無視設定
├── README.md                    # プロジェクト説明
├── DOCKER_README.md             # Docker説明
└── PROJECT_STRUCTURE.md         # このファイル
```

## 各コンポーネントの説明

### app/__init__.py
- アプリケーションファクトリパターンを実装
- 拡張機能の初期化
- Blueprintの登録
- エラーハンドラーの設定

### app/models/
各モデルファイルは独立しており、明確な責任を持ちます：
- `user.py`: ユーザー認証とプロフィール
- `project.py`: プロジェクトとメンバーシップ
- `knowledge.py`: ナレッジベースとコンテンツ
- `search_log.py`: 検索履歴とアナリティクス

### app/auth/
認証機能の完全なセット：
- `routes.py`: API エンドポイント
- `views.py`: Web ページビュー
- `services.py`: ビジネスロジック

### app/api/v1/
APIのバージョニング戦略：
- 将来のAPI変更に対応
- 下位互換性の維持
- 明確なエンドポイント構造

### app/utils/
再利用可能なユーティリティ：
- `decorators.py`: 認証、権限チェック
- `validators.py`: 入力値検証
- `logger.py`: ログ設定

### tests/
包括的なテストスイート：
- `conftest.py`: テスト共通設定
- 各機能のユニットテスト
- 統合テスト

## 設定とデプロイメント

### 開発環境
```bash
# 依存関係のインストール
./scripts/install_packages.sh

# 環境設定
./scripts/setup_env.sh

# アプリケーション起動
./scripts/run_app.sh
```

### Docker環境
```bash
# Docker Compose でスタック起動
docker-compose up -d

# ログ確認
docker-compose logs -f
```

### 本番環境
- `app.py` をWSGIサーバー（Gunicorn等）で実行
- 環境変数で設定を管理
- データベースマイグレーションの実行

## マイグレーション

新しい構造でのマイグレーション実行：
```bash
# マイグレーション作成
python scripts/migrate.py db init
python scripts/migrate.py db migrate -m "Initial migration"

# マイグレーション適用
python scripts/migrate.py db upgrade
```

## API エンドポイント

### 認証 API (v1)
- POST `/api/v1/auth/register` - ユーザー登録
- POST `/api/v1/auth/login` - ログイン
- POST `/api/v1/auth/logout` - ログアウト
- GET `/api/v1/auth/me` - 現在のユーザー情報

### プロジェクト API (v1)
- GET `/api/v1/projects` - プロジェクト一覧
- POST `/api/v1/projects` - プロジェクト作成
- GET `/api/v1/projects/{id}` - プロジェクト詳細
- PUT `/api/v1/projects/{id}` - プロジェクト更新
- DELETE `/api/v1/projects/{id}` - プロジェクト削除

### ナレッジベース API (v1)
- GET `/api/v1/knowledge` - ナレッジベース一覧
- POST `/api/v1/knowledge` - ナレッジベース作成
- GET `/api/v1/knowledge/{id}` - ナレッジベース詳細
- POST `/api/v1/knowledge/{id}/search` - 検索

## 今後の拡張計画

1. **APIバージョニング**: v2, v3の追加
2. **マイクロサービス**: 各モジュールの独立化
3. **キャッシュレイヤー**: Redis統合
4. **非同期処理**: Celery統合
5. **監視**: Prometheus + Grafana
6. **CI/CD**: GitHub Actions統合

この新しい構造により、プロジェクトの保守性、拡張性、テスタビリティが大幅に向上しました。
