#!/bin/bash

# SQLAlchemy対応のFlaskアプリケーション起動スクリプト
# 使用方法: ./run_app.sh [local|production]

ENV=${1:-local}

echo "SQLAlchemy対応アプリケーションを起動します..."

# 環境設定
./setup_env.sh $ENV

echo ""
echo "パッケージのインストール状況を確認中..."

# 必要なパッケージがインストールされているかチェック
python3 -c "
try:
    import flask, flask_sqlalchemy, flask_migrate, pymysql, dotenv
    print('✓ 必要なパッケージはすべてインストール済みです')
except ImportError as e:
    print('✗ 不足しているパッケージがあります:', e)
    print('次のコマンドで依存関係をインストールしてください:')
    print('pip install -r requirements.txt')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "依存関係の問題があります。アプリケーションを起動できません。"
    exit 1
fi

echo ""
echo "データベース接続テスト中..."

# データベース接続テスト
python3 -c "
from config import get_config
import os

try:
    config = get_config('$ENV')
    print('✓ 設定ファイルの読み込み成功')
    print(f'  環境: $ENV')
    print(f'  データベースURI: {config.SQLALCHEMY_DATABASE_URI.replace(config.DB_PASSWORD, \"***\")}')
except Exception as e:
    print('✗ 設定エラー:', e)
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "設定に問題があります。.env.${ENV} ファイルを確認してください。"
    exit 1
fi

echo ""
echo "🚀 Flaskアプリケーションを起動します..."
echo "   http://localhost:5000 でアクセスできます"
echo ""
echo "利用可能なエンドポイント:"
echo "  / - ホームページ"
echo "  /db-test - データベース接続テスト"
echo "  /config-info - 設定情報"
echo "  /init-db - データベース初期化"
echo "  /users - ユーザーAPI"
echo "  /knowledge - ナレッジAPI"
echo ""

# Flaskアプリケーション起動
export FLASK_APP=app.py
export FLASK_ENV=$ENV

python3 app.py
