# -*- coding: utf-8 -*-
"""
Flaskアプリケーションファクトリ
"""

import os
from flask import Flask, render_template_string

from .config import get_config
from .extensions import init_extensions


def create_app(config_name=None):
    """アプリケーションファクトリ"""
    app = Flask(__name__)
    
    # 設定を読み込み
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)
    
    # 拡張機能を初期化
    init_extensions(app)
    
    # Viteヘルパーを初期化
    from .utils.vite_helpers import init_vite_helpers
    init_vite_helpers(app)
    
    # Blueprintを登録
    register_blueprints(app)
    
    # エラーハンドラーを登録
    register_error_handlers(app)
    
    # メインルートを登録
    register_main_routes(app)
    
    return app


def register_blueprints(app):
    """Blueprintを登録"""
    from .main.views import main_bp
    from .auth.routes import auth_bp
    from .auth.views import auth_bp as auth_views_bp
    from .projects.routes import project_bp
    from .projects.views import project_bp as project_views_bp
    from .knowledge.views import knowledge_bp
    from .api.v1 import api_v1_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(auth_views_bp, name='auth_views')
    app.register_blueprint(project_bp)
    app.register_blueprint(project_views_bp, name='project_views')
    app.register_blueprint(knowledge_bp)
    app.register_blueprint(api_v1_bp)


def register_error_handlers(app):
    """エラーハンドラーを登録"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500


def register_main_routes(app):
    """メインルートを登録"""
    
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('main.index'))
    
    @app.route('/health')
    def health_check():
        """ヘルスチェックエンドポイント"""
        return {'status': 'healthy', 'version': '2.0.0'}


# アプリケーションの作成（開発サーバー用）
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
