#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flask-Migrate用のスクリプト

使用方法:
1. マイグレーション初期化: flask db init
2. マイグレーション生成: flask db migrate -m "コメント"
3. マイグレーション実行: flask db upgrade
"""

import os
from flask import current_app
from flask_migrate import Migrate
from app import create_app
from models import db

# 環境に応じたアプリケーション作成
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

# マイグレーション設定
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # データベース情報を表示
        print(f"Current environment: {config_name}")
        print(f"Database URI: {current_app.config['SQLALCHEMY_DATABASE_URI']}")
        print("Available commands:")
        print("  flask db init     - マイグレーション初期化")
        print("  flask db migrate  - マイグレーション生成")
        print("  flask db upgrade  - マイグレーション実行")
        print("  python migrate.py - この情報を表示")
