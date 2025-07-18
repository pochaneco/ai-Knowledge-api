# -*- coding: utf-8 -*-
"""
Viteアセット管理ヘルパー
"""

import json
import os
from flask import current_app, url_for


def vite_asset(path):
    """Viteビルド後のアセットパスを取得"""
    if current_app.config.get('ENV') == 'development':
        return f'http://localhost:3000/{path}'
    
    # プロダクション用のマニフェストファイルを読み込み
    manifest_path = os.path.join(current_app.static_folder, 'dist', 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
            if path in manifest:
                return url_for('static', filename=f"dist/{manifest[path]['file']}")
    
    return url_for('static', filename=f'dist/{path}')


def vite_hmr():
    """Vite HMR用スクリプトタグを生成"""
    if current_app.config.get('ENV') == 'development':
        return '''
        <script type="module" src="http://localhost:3000/@vite/client"></script>
        '''
    return ''


def init_vite_helpers(app):
    """Viteヘルパーをテンプレートグローバルに登録"""
    app.jinja_env.globals['vite_asset'] = vite_asset
    app.jinja_env.globals['vite_hmr'] = vite_hmr
