# -*- coding: utf-8 -*-
"""
Flask拡張機能の初期化
"""

from flask_migrate import Migrate
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

# 拡張機能のインスタンス
migrate = Migrate()
login_manager = LoginManager()
oauth = OAuth()


def init_extensions(app):
    """Flask拡張機能を初期化"""
    from app.models import db, User
    from app.email import init_mail
    from app.inertia_config import init_inertia
    
    # データベース初期化
    db.init_app(app)
    
    # マイグレーション初期化
    migrate.init_app(app, db)
    
    # Inertia.js初期化
    inertia = init_inertia(app)
    
    # Flask-Login初期化
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'ログインが必要です'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import db
        return db.session.get(User, int(user_id))
    
    # メールサービス初期化
    init_mail(app)
    
    # OAuth初期化
    oauth.init_app(app)
    
    # Google OAuth設定
    google = oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    return google, inertia
