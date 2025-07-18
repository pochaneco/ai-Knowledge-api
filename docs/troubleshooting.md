# トラブルシューティングガイド

AI Knowledge APIでよく発生する問題とその解決方法をまとめています。

## 🐳 Docker関連の問題

### 1. ポート競合エラー

**エラーメッセージ:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:5000: bind: address already in use
```

**解決方法:**
```bash
# 使用中のポートを確認
netstat -tlnp | grep :5000
# または
lsof -i :5000

# プロセスを停止
kill -9 <PID>

# または .env ファイルでポート番号を変更
WEB_API_PORT=5000
VITE_PORT=5173
```

### 2. データベース接続エラー

**エラーメッセージ:**
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")
```

**解決方法:**
```bash
```bash
# データベースコンテナの状態確認
docker-compose ps db

# データベースログの確認
docker-compose logs db
```

# データベースコンテナの再起動
docker-compose -f docker-compose.dev.yml restart db

# 完全な再構築
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

### 3. フロントエンドビルドエラー

**エラーメッセージ:**
```
Module not found: Can't resolve '@/components/...'
```

**解決方法:**
```bash
# node_modulesの再インストール
docker-compose exec frontend rm -rf node_modules package-lock.json
docker-compose exec frontend npm install

# キャッシュクリア
docker-compose exec frontend npm run dev -- --force
```

### 4. パーミッションエラー

**エラーメッセージ:**
```
Permission denied: '/app/...'
```

**解決方法:**
```bash
# ファイルの所有者を確認・変更
sudo chown -R $USER:$USER .

# Dockerコンテナ内での実行ユーザーを確認
docker-compose -f docker-compose.dev.yml exec web whoami
```

## 🐍 Python/Flask関連の問題

### 1. モジュールインポートエラー

**エラーメッセージ:**
```
ModuleNotFoundError: No module named 'app'
```

**解決方法:**
```bash
# 仮想環境の有効化確認
source .venv/bin/activate

# PYTHONPATHの設定
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 依存関係の再インストール
pip install -r requirements.txt
```

### 2. データベースマイグレーションエラー

**エラーメッセージ:**
```
Target database is not up to date
```

**解決方法:**
```bash
# 現在のマイグレーション状態を確認
flask db current

# マイグレーション履歴を確認
flask db history

# 強制的にリビジョンを設定（危険：データ損失の可能性）
flask db stamp head

# 安全なマイグレーション
flask db upgrade
```

### 3. 環境変数読み込みエラー

**エラーメッセージ:**
```
KeyError: 'SECRET_KEY'
```

**解決方法:**
```bash
# 環境変数の確認
echo $SECRET_KEY

# 環境ファイルの確認
cat .env        # Docker環境
cat .env.local  # ローカル環境

# 環境ファイルの作成（必要に応じて）
cp .env.example .env
cp .env.docker.example .env  # Docker用

# 環境変数の手動設定
export SECRET_KEY=your-secret-key

# .env ファイルの読み込み
export $(cat .env | xargs)        # Docker環境
export $(cat .env.local | xargs)  # ローカル環境
```

## 🎨 フロントエンド関連の問題

### 1. Viteビルドエラー

**エラーメッセージ:**
```
Error: Cannot resolve dependency
```

**解決方法:**
```bash
# 依存関係の確認
npm ls

# package-lock.jsonの削除と再インストール
rm package-lock.json
rm -rf node_modules
npm install

# Viteキャッシュクリア
rm -rf node_modules/.vite
```

### 2. Inertia.js レンダリングエラー

**エラーメッセージ:**
```
Inertia page not found
```

**解決方法:**
```javascript
// ページコンポーネントの登録確認
// frontend/src/app.js
import { createInertiaApp } from '@inertiajs/vue3'

createInertiaApp({
  resolve: name => {
    const pages = import.meta.glob('./pages/**/*.vue', { eager: true })
    return pages[`./pages/${name}.vue`]
  },
  // ...
})
```

### 3. CSS/Tailwindスタイルエラー

**エラーメッセージ:**
```
Unknown at rule @tailwind
```

**解決方法:**
```bash
# Tailwind CSSの再インストール
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

# 設定ファイルの確認
cat tailwind.config.js
cat postcss.config.js
```

## 🗄️ データベース関連の問題

### 1. MySQL接続タイムアウト

**エラーメッセージ:**
```
Lost connection to MySQL server during query
```

**解決方法:**
```bash
# MySQLの設定確認
docker-compose -f docker-compose.dev.yml exec db mysql -u root -p -e "SHOW VARIABLES LIKE 'wait_timeout';"

# 接続プールの設定
# app/config.py に追加
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

### 2. 文字化け問題

**エラーメッセージ:**
```
Incorrect string value: '\xE2\x9C...' for column
```

**解決方法:**
```sql
-- データベースの文字セット確認
SHOW VARIABLES LIKE 'character_set%';

-- テーブルの文字セット変更
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. インデックスエラー

**エラーメッセージ:**
```
Duplicate key name
```

**解決方法:**
```sql
-- 既存のインデックス確認
SHOW INDEX FROM table_name;

-- インデックスの削除
DROP INDEX index_name ON table_name;
```

## 🔐 認証・セキュリティ関連の問題

### 1. Google OAuth エラー

**エラーメッセージ:**
```
invalid_client: The OAuth client was not found
```

**解決方法:**
```bash
# 環境変数の確認
echo $GOOGLE_CLIENT_ID
echo $GOOGLE_CLIENT_SECRET

# Google Cloud Console での設定確認
# - クライアントIDの正確性
# - リダイレクトURIの設定
# - APIの有効化状況
```

### 2. セッション関連エラー

**エラーメッセージ:**
```
The session is either invalid or has expired
```

**解決方法:**
```python
# app/config.py でセッション設定を確認
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
SESSION_COOKIE_SECURE = True  # HTTPS環境でのみ
SESSION_COOKIE_HTTPONLY = True
```

## 🚀 デプロイ関連の問題

### 1. Gunicorn起動エラー

**エラーメッセージ:**
```
ModuleNotFoundError: No module named 'app'
```

**解決方法:**
```bash
# Gunicornの設定確認
# gunicorn.conf.py
pythonpath = '/var/www/ai-knowledge-api'

# 手動でGunicornを起動してテスト
cd /var/www/ai-knowledge-api
gunicorn -c gunicorn.conf.py app:app
```

### 2. Nginx 502 Bad Gateway

**解決方法:**
```bash
# Gunicornサービスの状態確認
sudo systemctl status ai-knowledge-api

# Nginxエラーログの確認
sudo tail -f /var/log/nginx/error.log

# アップストリーム接続の確認
curl -I http://127.0.0.1:8000
```

### 3. SSL証明書エラー

**解決方法:**
```bash
# 証明書の有効期限確認
openssl x509 -in /path/to/cert.pem -text -noout | grep "Not After"

# Let's Encrypt証明書の更新
sudo certbot renew --dry-run
sudo certbot renew
```

## 🔧 パフォーマンス関連の問題

### 1. データベースクエリが遅い

**解決方法:**
```python
# SQLAlchemyのクエリログを有効化
SQLALCHEMY_ECHO = True

# クエリの最適化
# N+1問題の解決
users = User.query.options(joinedload(User.projects)).all()

# インデックスの追加
class User(db.Model):
    email = db.Column(db.String(255), index=True)
```

### 2. メモリ使用量が多い

**解決方法:**
```bash
# プロセスのメモリ使用量確認
ps aux | grep python

# Pythonのメモリプロファイリング
pip install memory-profiler
python -m memory_profiler app.py
```

## 🧪 テスト関連の問題

### 1. テストデータベース作成エラー

**解決方法:**
```python
# tests/conftest.py
@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

### 2. Docker環境でのテスト実行エラー

**エラーメッセージ:**
```
ModuleNotFoundError: No module named 'app'
```

**解決方法:**
```bash
# PYTHONPATHを明示的に設定
docker run --rm -v $(pwd):/app -w /app ai-knowledge-test sh -c "PYTHONPATH=/app pytest -v"

# または、Docker Composeで環境変数を設定
environment:
  - PYTHONPATH=/app
```

### 3. SQLAlchemy DetachedInstanceError

**エラーメッセージ:**
```
DetachedInstanceError: Instance is not bound to a Session
```

**解決方法:**
```python
# テストフィクスチャで適切なセッション管理
@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(email='test@example.com')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    # 新しいコンテキストでオブジェクトを取得
    with app.app_context():
        return db.session.get(User, user_id)
```

### 4. MySQL統合テスト接続エラー

**エラーメッセージ:**
```
Access denied for user 'app_user'@'%' to database 'test_ai_knowledge_db'
```

**解決方法:**
```bash
# rootユーザーでテストDB作成
mysql -h db -u root -proot_password -e "CREATE DATABASE IF NOT EXISTS test_ai_knowledge_db; GRANT ALL PRIVILEGES ON test_ai_knowledge_db.* TO 'app_user'@'%';"

# またはDocker Composeでroot権限使用
command: >
  sh -c "
    mysql -h db -u root -p${MYSQL_ROOT_PASSWORD} -e 'CREATE DATABASE IF NOT EXISTS test_${DB_NAME}; GRANT ALL PRIVILEGES ON test_${DB_NAME}.* TO \"${DB_USER}\"@\"%\";' &&
    pytest -v
  "
```

### 5. テスト実行時の認証エラー

**解決方法:**
```python
# tests/conftest.py
@pytest.fixture
def authenticated_user(client):
    user = User(email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)
        sess['_fresh'] = True
    
    return user
```

## 📞 サポート

### 一般的なトラブルシューティング手順

1. **エラーメッセージの確認**: 詳細なエラーメッセージを記録
2. **ログの確認**: アプリケーション、サーバー、データベースのログを確認
3. **環境の確認**: 環境変数、設定ファイル、依存関係のバージョンを確認
4. **再現手順の記録**: 問題を再現するための具体的な手順を記録

### 問題報告時の情報

- オペレーティングシステム
- Python/Node.jsのバージョン
- エラーメッセージの全文
- 実行したコマンド
- 関連する設定ファイル
- ログファイルの内容

### 追加リソース

- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Vue.js公式ドキュメント](https://vuejs.org/)
- [Docker公式ドキュメント](https://docs.docker.com/)
- [MySQL公式ドキュメント](https://dev.mysql.com/doc/)
