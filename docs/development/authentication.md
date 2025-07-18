# AI Knowledge API 🚀

ユーザー認証、プロジェクト管理、チーム招待機能を備えたナレッジベース管理APIです。

## ✨ 主な機能

### 🔐 認証機能
- **ユーザー登録・ログイン**: メールアドレスとパスワードによる認証
- **Google OAuth**: Googleアカウントでのソーシャルログイン
- **メール認証**: 登録時のメールアドレス認証機能
- **パスワードリセット**: 忘れたパスワードのリセット機能

### 📁 プロジェクト管理
- **プロジェクト作成**: チーム用のプロジェクト作成
- **メンバー招待**: メールでチームメンバーを招待
- **権限管理**: オーナー、管理者、メンバーの3段階権限
- **プライベート/パブリック**: プロジェクトの公開設定

### 📚 ナレッジベース
- **プロジェクト内管理**: プロジェクト別のナレッジ管理
- **カテゴリ分類**: ナレッジのカテゴリ整理
- **タグ機能**: 柔軟なタグ付けシステム
- **検索機能**: タイトル・内容での全文検索

## 🛠️ 技術スタック

- **バックエンド**: Flask + SQLAlchemy
- **データベース**: MySQL 8.0
- **認証**: Flask-Login + Authlib (Google OAuth)
- **メール**: Flask-Mail
- **マイグレーション**: Flask-Migrate
- **パスワード暗号化**: bcrypt
- **トークン管理**: itsdangerous

## 🚀 クイックスタート

### 1. Docker Composeを使用（推奨）

```bash
# リポジトリをクローン
git clone <repository-url>
cd ai-Knowledge-api

# 環境変数を設定
cp .env.docker .env.local

# Docker Composeでサービスを起動
docker-compose up -d

# マイグレーションを実行
docker-compose exec web flask db init
docker-compose exec web flask db migrate -m "Initial migration"
docker-compose exec web flask db upgrade
```

### 2. ローカル開発環境

```bash
# 仮想環境を作成
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env.local
# .env.local を編集して適切な値を設定

# データベースマイグレーション
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# アプリケーションを起動
python app.py
```

## 📋 API エンドポイント

### 認証API
- `POST /auth/register` - ユーザー登録
- `POST /auth/login` - ログイン
- `POST /auth/logout` - ログアウト
- `GET /auth/google` - Google OAuth認証開始
- `GET /auth/google/callback` - Google OAuth コールバック
- `GET /auth/verify-email/<token>` - メールアドレス認証
- `POST /auth/forgot-password` - パスワードリセット要求
- `POST /auth/reset-password/<token>` - パスワードリセット実行
- `GET /auth/me` - 現在のユーザー情報取得

### プロジェクトAPI
- `GET /projects` - ユーザーのプロジェクト一覧
- `POST /projects` - プロジェクト作成
- `GET /projects/{id}` - プロジェクト詳細
- `PUT /projects/{id}` - プロジェクト更新
- `DELETE /projects/{id}` - プロジェクト削除
- `POST /projects/{id}/invite` - メンバー招待
- `GET /projects/{id}/members` - メンバー一覧
- `DELETE /projects/{id}/members/{user_id}` - メンバー削除
- `GET /projects/{id}/knowledge` - プロジェクトのナレッジ一覧

## 🔧 設定

### 環境変数

| 変数名 | 説明 | 必須 |
|--------|------|------|
| `SECRET_KEY` | Flaskの秘密鍵 | ✅ |
| `DB_HOST` | データベースホスト | ✅ |
| `DB_USER` | データベースユーザー | ✅ |
| `DB_PASSWORD` | データベースパスワード | ✅ |
| `DB_NAME` | データベース名 | ✅ |
| `MAIL_SERVER` | SMTPサーバー | ✅ |
| `MAIL_USERNAME` | メールユーザー名 | ✅ |
| `MAIL_PASSWORD` | メールパスワード | ✅ |
| `GOOGLE_CLIENT_ID` | Google OAuth クライアントID | ⭕ |
| `GOOGLE_CLIENT_SECRET` | Google OAuth クライアントシークレット | ⭕ |

### Google OAuth設定

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. OAuth 2.0 認証情報を作成
3. 認証済みリダイレクトURIに以下を追加:
   - `http://localhost:5000/auth/google/callback` (開発用)
   - `https://yourdomain.com/auth/google/callback` (本番用)

## 🏗️ アーキテクチャ

```
ai-Knowledge-api/
├── app.py                 # メインアプリケーション
├── models.py             # データベースモデル
├── config.py             # 設定管理
├── auth_service.py       # 認証サービス
├── auth_routes.py        # 認証エンドポイント
├── project_service.py    # プロジェクトサービス
├── project_routes.py     # プロジェクトエンドポイント
├── email_service.py      # メール送信サービス
├── migrate.py            # マイグレーション管理
├── requirements.txt      # Python依存関係
├── docker-compose.yml    # Docker Compose設定
├── Dockerfile           # Dockerイメージ定義
└── .env.example         # 環境変数テンプレート
```

## 🧪 テスト

```bash
# テストを実行
python -m pytest tests/

# カバレッジレポート付き
python -m pytest tests/ --cov=.
```

## 📦 デプロイ

### Docker Composeでの本番デプロイ

```bash
# 本番用環境変数を設定
cp .env.example .env.production
# .env.production を編集

# 本番環境で起動
FLASK_ENV=production docker-compose up -d
```

## 🤝 コントリビューション

1. フォークする
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

MIT License

## 🔗 関連リンク

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
