# Python venv環境セットアップガイド

Python仮想環境を使用したローカル開発環境のセットアップ方法です。

## 📋 前提条件

- Python 3.8以上
- MySQL 8.0
- Node.js 16以上
- npm または yarn

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/pochaneco/vidays.git
cd vidays
```

### 2. Python仮想環境の作成

```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 3. Python依存関係のインストール

```bash
# 基本パッケージのインストール
pip install -r requirements.txt

# 開発用パッケージのインストール（オプション）
pip install -r requirements-dev.txt
```

### 4. Node.js依存関係のインストール

```bash
# フロントエンド依存関係のインストール
npm install

# または yarn を使用
yarn install
```

### 5. データベースの準備

#### MySQLの起動とデータベース作成

```bash
# MySQLサーバーの起動（macOS with Homebrew）
brew services start mysql

# MySQLサーバーの起動（Ubuntu/Debian）
sudo systemctl start mysql

# データベースとユーザーの作成
mysql -u root -p
```

```sql
-- データベースの作成
CREATE DATABASE ai_knowledge_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ユーザーの作成と権限付与
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'app_password';
GRANT ALL PRIVILEGES ON ai_knowledge_db.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;

EXIT;
```

### 6. 環境変数の設定

```bash
# 環境変数ファイルのコピー
cp .env.example .env.local

# .env.local ファイルの編集
vim .env.local
```

**重要な設定項目:**

```env
# データベース接続（ローカル）
DB_HOST=localhost
DB_PORT=3306
DB_USER=app_user
DB_PASSWORD=app_password
DB_NAME=ai_knowledge_db

# Flask設定
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-development-secret-key

# Viteポート設定
VITE_PORT=5173
```

### 7. データベースマイグレーション

```bash
# 環境変数の読み込み
export $(cat .env.local | xargs)

# マイグレーションの初期化（初回のみ）
flask db init

# マイグレーションファイルの生成
flask db migrate -m "Initial migration"

# マイグレーションの適用
flask db upgrade
```

## 🚀 アプリケーションの起動

### バックエンド（Flask）の起動

```bash
# 仮想環境が有効化されていることを確認
source .venv/bin/activate

# 環境変数の設定
export $(cat .env.local | xargs)

# Flaskアプリケーションの起動
python app.py

# または
flask run
```

### フロントエンド（Vite）の起動

```bash
# 別のターミナルで実行
npm run dev

# または
yarn dev
```

## 🌐 アクセス方法

- **バックエンドAPI**: http://localhost:5000
- **フロントエンド**: http://localhost:5173

## 🛠️ 開発コマンド

### データベース操作

```bash
# マイグレーションファイルの生成
flask db migrate -m "説明"

# マイグレーションの適用
flask db upgrade

# マイグレーション履歴の確認
flask db history

# 現在のリビジョンの確認
flask db current
```

### テストの実行

```bash
# 全テストの実行（SQLiteインメモリ、高速）
pytest

# 詳細出力付きテスト
pytest -v

# 特定のテストファイルの実行
pytest tests/test_auth.py

# カバレッジ付きでテスト実行
pytest --cov=app --cov-report=term-missing --cov-report=html

# 継続的テスト実行（ファイル変更を監視）
pytest-watch
```

### Docker環境との比較

| 実行環境 | セットアップ時間 | テスト実行時間 | メモリ使用量 | 推奨用途 |
|----------|------------------|----------------|--------------|----------|
| venv | 初回のみ5分 | 3秒 | 低 | 日常開発 |
| Docker | 毎回1-2分 | 16秒 | 高 | CI/CD、統合テスト |

**推奨**: 日常開発はvenv環境、CI/CDやチーム統一環境にはDockerを使用

### フロントエンドビルド

```bash
# 開発用ビルド
npm run dev

# 本番用ビルド
npm run build

# ビルドファイルのプレビュー
npm run preview
```

## 🔧 設定のカスタマイズ

### デバッグモードの有効化

`.env.local`で以下を設定：

```env
FLASK_DEBUG=True
SQLALCHEMY_ECHO=True  # SQLクエリのログ出力
```

### メール設定（開発用）

```env
# Gmail SMTPの例
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

### Google OAuth設定

Google Cloud Consoleで設定したクライアント情報を追加：

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## 📝 トラブルシューティング

### Python仮想環境の問題

```bash
# 仮想環境の削除と再作成
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### データベース接続エラー

```bash
# MySQLサービスの状態確認
brew services list | grep mysql  # macOS
systemctl status mysql           # Linux

# データベース接続テスト
mysql -u app_user -p -h localhost ai_knowledge_db
```

### ポート競合エラー

```bash
# 使用中のポートを確認
netstat -tlnp | grep :5000
netstat -tlnp | grep :5173

# 別のポート番号を使用
export FLASK_RUN_PORT=5001
export VITE_PORT=5174
```

### Node.js依存関係の問題

```bash
# node_modulesの削除と再インストール
rm -rf node_modules
rm package-lock.json
npm install
```

## 🔄 開発ワークフロー

1. **仮想環境の有効化**
   ```bash
   source .venv/bin/activate
   ```

2. **環境変数の設定**
   ```bash
   export $(cat .env.local | xargs)
   ```

3. **両方のサーバーを起動**
   ```bash
   # ターミナル1: バックエンド
   python app.py
   
   # ターミナル2: フロントエンド
   npm run dev
   ```

4. **開発作業**
   - バックエンド: `app/` ディレクトリでPythonコードを編集
   - フロントエンド: `frontend/src/` ディレクトリでVue.jsコードを編集

5. **テストの実行**
   ```bash
   pytest
   ```
