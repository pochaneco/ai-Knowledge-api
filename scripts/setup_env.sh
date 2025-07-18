#!/bin/bash

# 環境設定スクリプト
# 使用方法: ./setup_env.sh [local|production]

ENV=${1:-local}

echo "環境を '$ENV' に設定します..."

case $ENV in
    "local")
        if [ -f ".env.local" ]; then
            cp .env.local .env
            echo "ローカル環境設定を適用しました (.env.local -> .env)"
        else
            echo "エラー: .env.local ファイルが見つかりません"
            echo ".env.example をコピーして .env.local を作成してください"
            exit 1
        fi
        ;;
    "production")
        if [ -f ".env.production" ]; then
            cp .env.production .env
            echo "本番環境設定を適用しました (.env.production -> .env)"
        else
            echo "エラー: .env.production ファイルが見つかりません"
            echo ".env.example をコピーして .env.production を作成してください"
            exit 1
        fi
        ;;
    *)
        echo "エラー: 無効な環境名です"
        echo "使用方法: ./setup_env.sh [local|production]"
        exit 1
        ;;
esac

echo "現在の設定:"
echo "FLASK_ENV=$(grep FLASK_ENV .env | cut -d'=' -f2)"
echo "DB_HOST=$(grep DB_HOST .env | cut -d'=' -f2)"
echo "DB_NAME=$(grep DB_NAME .env | cut -d'=' -f2)"
