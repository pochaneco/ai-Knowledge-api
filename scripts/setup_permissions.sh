#!/bin/bash

echo "ファイルとフォルダの権限を設定しています..."

# スクリプトファイルに実行権限を付与
echo "スクリプトファイルの権限設定..."
chmod +x scripts/*.sh
chmod +x index.cgi

# Python仮想環境の権限設定
if [ -d ".venv" ]; then
    echo "Python仮想環境の権限設定..."
    chmod +x .venv/bin/*
    find .venv -type d -exec chmod 755 {} \;
    find .venv -type f -exec chmod 644 {} \;
    chmod +x .venv/bin/activate
    chmod +x .venv/bin/python*
    chmod +x .venv/bin/pip*
fi

# Pythonファイルの権限設定
echo "Pythonファイルの権限設定..."
find . -name "*.py" -type f -exec chmod 644 {} \;
chmod +x app.py

# 設定ファイルの権限設定
echo "設定ファイルの権限設定..."
chmod 644 requirements.txt
chmod 644 docker-compose.yml
chmod 644 Dockerfile
if [ -f ".htaccess" ]; then
    chmod 644 .htaccess
fi

# 環境設定ファイルの権限（セキュリティのため制限的に）
echo "環境設定ファイルの権限設定..."
find . -name ".env*" -type f -exec chmod 600 {} \;

# ディレクトリの権限設定
echo "ディレクトリの権限設定..."
find . -type d -exec chmod 755 {} \;

# ログファイルとデータディレクトリの権限（存在する場合）
if [ -d "logs" ]; then
    chmod 755 logs
    find logs -type f -exec chmod 644 {} \;
fi

if [ -d "data" ]; then
    chmod 755 data
    find data -type f -exec chmod 644 {} \;
fi

# Viteビルド出力ディレクトリの権限設定
echo "Viteビルド出力ディレクトリの権限設定..."
if [ -d "app/static" ]; then
    chmod 755 app/static
    if [ -d "app/static/dist" ]; then
        chmod 755 app/static/dist
        find app/static/dist -type f -exec chmod 644 {} \;
        find app/static/dist -type d -exec chmod 755 {} \;
    else
        mkdir -p app/static/dist
        chmod 755 app/static/dist
    fi
fi

echo "権限設定完了！"
echo ""
echo "主要なファイル・フォルダの権限:"
ls -la
echo ""
echo "スクリプトファイルの権限:"
ls -la scripts/
if [ -d ".venv" ]; then
    echo ""
    echo "仮想環境の権限:"
    ls -la .venv/bin/ | head -10
fi
