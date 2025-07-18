#!/bin/bash

# ユーザーディレクトリにパッケージをインストール
echo "Python パッケージをインストールしています..."

# requirements.txtからパッケージをインストール
~/.local/bin/pip3 install --user -r requirements.txt

echo "インストール完了！"
echo "以下のコマンドでパスを確認してください："
echo "python3 -c \"import sys; print(sys.path)\""
