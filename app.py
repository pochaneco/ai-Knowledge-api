#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vidays エントリーポイント

新しいモジュール化された構造を使用したFlaskアプリケーション
"""

from app import create_app

# アプリケーションファクトリから作成
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
