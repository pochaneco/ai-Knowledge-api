# -*- coding: utf-8 -*-
"""
Inertia.js設定（独自実装）
"""

import json
from flask import request, render_template, session, make_response
from flask_login import current_user


class InertiaFlask:
    def __init__(self, app=None):
        self.app = app
        self.shared_data = {}
        self.version = '1.0.0'
        self.template = 'app.html'
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Flaskアプリケーションに初期化"""
        app.config.setdefault('INERTIA_TEMPLATE', 'app.html')
        app.config.setdefault('INERTIA_VERSION', '1.0.0')
        
        # テンプレートグローバルにrender関数を追加
        app.jinja_env.globals['inertia_render'] = self.render
        
        @app.context_processor
        def inject_inertia():
            return {
                'inertia_render': self.render
            }
    
    def share(self, func=None, **kwargs):
        """共有データを設定"""
        if func:
            self.shared_data.update(func())
        else:
            self.shared_data.update(kwargs)
        return func
    
    def render(self, component, props=None):
        """Inertiaレスポンスを生成"""
        if props is None:
            props = {}
        
        # 共有データを取得
        shared = self.get_shared_data()
        
        # ページデータを作成
        page_data = {
            'component': component,
            'props': {**shared, **props},
            'url': request.url,
            'version': self.version,
        }
        
        # InertiaリクエストかHTMLリクエストかを判定
        if request.headers.get('X-Inertia'):
            # Inertiaリクエストの場合はJSONレスポンス
            response = make_response(json.dumps(page_data))
            response.headers['Content-Type'] = 'application/json'
            response.headers['Vary'] = 'Accept'
            response.headers['X-Inertia'] = 'true'
            return response
        else:
            # 通常のHTMLリクエストの場合
            return render_template(self.template, page=json.dumps(page_data))
    
    def get_shared_data(self):
        """共有データを取得"""
        shared_data = {
            'csrf_token': session.get('csrf_token'),
            'flash': {
                'success': session.pop('flash_success', None),
                'error': session.pop('flash_error', None),
                'info': session.pop('flash_info', None),
            }
        }
        
        # ユーザー情報を共有
        if current_user.is_authenticated:
            shared_data['auth'] = {
                'user': {
                    'id': current_user.id,
                    'username': current_user.username,
                    'email': current_user.email,
                    'display_name': getattr(current_user, 'display_name', None),
                }
            }
        else:
            shared_data['auth'] = {
                'user': None
            }
        
        return shared_data


# グローバルインスタンス
inertia = InertiaFlask()


def init_inertia(app):
    """Inertia.jsを初期化"""
    inertia.init_app(app)
    return inertia


def render(component, props=None):
    """Inertiaレンダー関数（ショートカット）"""
    return inertia.render(component, props)
