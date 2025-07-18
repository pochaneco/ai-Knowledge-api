# AI Knowledge API

AI知識管理システムです。プロジェクトごとに知識を管理し、チームメンバーと共有できます。

## 🚀 特徴

- **マルチプロジェクト対応**: プロジェクトごとに知識を分離管理
- **チーム機能**: メンバー招待とロールベースアクセス制御
- **REST API**: 完全なAPI機能
- **モダンUI**: Inertia.js + Vue.js によるSPA体験
- **認証機能**: パスワード認証 + Google OAuth
- **レスポンシブ**: Tailwind CSS によるモダンなデザイン

## 🛠️ 技術スタック

### バックエンド
- **Flask**: Python Webフレームワーク
- **SQLAlchemy**: ORM
- **Flask-Migrate**: データベースマイグレーション
- **Flask-Login**: 認証管理
- **Authlib**: OAuth実装

### フロントエンド
- **Inertia.js**: SPA体験の提供
- **Vue.js 3**: リアクティブUI
- **Tailwind CSS**: ユーティリティファーストCSS
- **Vite**: 高速ビルドツール

### データベース
- **MySQL 8.0**: メインデータベース

## 📖 セットアップガイド

開発環境に応じて適切なセットアップ方法を選択してください：

### 🐳 Docker環境（推奨）
```bash
# 詳細なセットアップ手順
cat docs/setup/docker-setup.md

# クイックスタート
make setup-docker        # セットアップ
make docker-dev          # 開発モード起動
# または
docker-compose --profile dev up -d
```
**推奨理由**: 環境の統一、依存関係の自動解決、データベースの自動セットアップ

### 🐍 Python venv環境
```bash
# 詳細なセットアップ手順
cat docs/setup/venv-setup.md
```
**適用場面**: ローカルでの詳細な開発、デバッグ作業

### 🖥️ サーバー環境
```bash
# 詳細なセットアップ手順
cat docs/setup/server-setup.md
```
**適用場面**: 本番デプロイ、共用レンタルサーバー

## 🔗 クイックスタート

1. リポジトリをクローン
   ```bash
   git clone https://github.com/pochaneco/ai-Knowledge-api.git
   cd ai-Knowledge-api
   ```

2. 環境を選択してセットアップ
   - Docker: `docs/setup/docker-setup.md`
   - venv: `docs/setup/venv-setup.md`

3. テスト実行
   ```bash
   # ローカル環境（高速）
   make test
   
   # Docker環境（CI/CD）
   make test-docker
   
   # 全コマンド確認
   make help
   ```
   - Server: `docs/setup/server-setup.md`

3. ブラウザでアクセス
   ```
   http://localhost:5000   # Docker（デフォルト）
   http://localhost:5000   # venv
   ```

## 📚 ドキュメント

- [開発ガイド](docs/development/)
- [API仕様](docs/api/)
- [アーキテクチャ](docs/architecture/)
- [トラブルシューティング](docs/troubleshooting.md)

## 🤝 コントリビューション

プルリクエストは歓迎します。大きな変更の場合は、まずIssueで相談してください。

## 📄 ライセンス

MIT License
