#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from wsgiref.handlers import CGIHandler
from dotenv import load_dotenv

# .envファイルをロード
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    # print(f"環境変数をロードしました: {env_path}")
else:
    print("警告: .envファイルが見つかりません")
  
# パスの設定
sys.path.insert(0, os.path.dirname(__file__))

# Flaskアプリケーションをインポート
from app import app

if __name__ == '__main__':
    CGIHandler().run(app)
