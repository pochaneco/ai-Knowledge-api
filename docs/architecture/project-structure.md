# Vidays - 推奨ディレクトリ構造

```
vidays/
├── app/                          # メインアプリケーションディレクトリ
│   ├── __init__.py              # アプリケーションファクトリ
│   ├── models/                  # データベースモデル
│   │   ├── __init__.py
│   │   ├── user.py             # ユーザーモデル
│   │   ├── project.py          # プロジェクトモデル
│   │   ├── knowledge.py        # ナレッジベースモデル
│   │   └── search_log.py       # 検索ログモデル
│   ├── auth/                    # 認証関連
│   │   ├── __init__.py
│   │   ├── routes.py           # 認証エンドポイント
│   │   ├── services.py         # 認証サービス
│   │   └── forms.py            # 認証フォーム（WTForms）
│   ├── projects/                # プロジェクト関連
│   │   ├── __init__.py
│   │   ├── routes.py           # プロジェクトエンドポイント
│   │   ├── services.py         # プロジェクトサービス
│   │   └── forms.py            # プロジェクトフォーム
│   ├── knowledge/               # ナレッジベース関連
│   │   ├── __init__.py
│   │   ├── routes.py           # ナレッジエンドポイント
│   │   ├── services.py         # ナレッジサービス
│   │   └── forms.py            # ナレッジフォーム
│   ├── api/                     # API関連
│   │   ├── __init__.py
│   │   ├── v1/                 # APIバージョン1
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # API認証エンドポイント
│   │   │   ├── projects.py     # APIプロジェクトエンドポイント
│   │   │   └── knowledge.py    # APIナレッジエンドポイント
│   │   └── errors.py           # API エラーハンドラー
│   ├── email/                   # メール関連
│   │   ├── __init__.py
│   │   ├── services.py         # メール送信サービス
│   │   └── templates/          # メールテンプレート
│   │       ├── auth/
│   │       │   ├── verify_email.html
│   │       │   └── reset_password.html
│   │       └── projects/
│   │           └── invitation.html
│   ├── static/                  # 静的ファイル
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/               # HTMLテンプレート
│   │   ├── base.html
│   │   ├── index.html
│   │   └── auth/
│   │       ├── login.html
│   │       └── register.html
│   ├── utils/                   # ユーティリティ
│   │   ├── __init__.py
│   │   ├── decorators.py       # カスタムデコレータ
│   │   ├── validators.py       # バリデータ
│   │   └── helpers.py          # ヘルパー関数
│   ├── extensions.py            # Flask拡張機能の初期化
│   └── config.py               # 設定クラス
├── migrations/                  # データベースマイグレーション
├── tests/                       # テストファイル
│   ├── __init__.py
│   ├── conftest.py             # pytest設定
│   ├── test_auth.py            # 認証テスト
│   ├── test_projects.py        # プロジェクトテスト
│   └── test_knowledge.py       # ナレッジテスト
├── docker/                      # Docker関連ファイル
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── mysql/
│   │   └── init/
│   │       └── 01-init.sql
│   └── nginx/                  # 本番用Nginx設定
│       └── nginx.conf
├── scripts/                     # スクリプトファイル
│   ├── setup_env.sh
│   ├── run_app.sh
│   ├── migrate.py
│   └── seed_data.py            # サンプルデータ投入
├── docs/                        # ドキュメント
│   ├── api.md                  # API仕様
│   ├── setup.md               # セットアップガイド
│   └── deployment.md          # デプロイガイド
├── .env.example                # 環境変数テンプレート
├── .env.docker                 # Docker用環境変数
├── .gitignore
├── requirements.txt            # Python依存関係
├── requirements-dev.txt        # 開発用依存関係
├── pyproject.toml             # Python プロジェクト設定
├── pytest.ini                # pytest設定
├── Dockerfile
├── docker-compose.yml
├── app.py                     # アプリケーションエントリーポイント
└── README.md
```

## 各ディレクトリの役割

### `/app/` - メインアプリケーション
- アプリケーションロジックの中核
- 機能別にモジュール分割

### `/app/models/` - データベースモデル
- SQLAlchemyモデルを機能別に分割
- リレーションシップの管理を明確化

### `/app/auth/`, `/app/projects/`, `/app/knowledge/` - 機能別モジュール
- 各機能のルート、サービス、フォームを統合
- 機能の独立性を保持

### `/app/api/` - API専用モジュール
- バージョン管理対応のAPI構造
- RESTful APIの実装

### `/tests/` - テストスイート
- 機能別テストファイル
- 統合テストとユニットテスト

### `/docker/` - コンテナ関連
- Dockerファイルとコンテナ設定
- 環境別の設定ファイル

### `/scripts/` - ユーティリティスクリプト
- 開発・運用で使用するスクリプト
- データベース管理スクリプト

## この構造の利点

1. **明確な責任分離**: 各モジュールが特定の機能を担当
2. **スケーラビリティ**: 新機能の追加が容易
3. **テスタビリティ**: テストしやすい構造
4. **保守性**: コードの場所が予測しやすい
5. **チーム開発**: 並行開発時の競合を最小化
