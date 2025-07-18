#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
認証関連のBlueprint
ログイン、ログアウト、ユーザー登録、メール認証などのエンドポイント
"""

from flask import Blueprint, request, jsonify, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from ..models import db, User
from .services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# OAuth設定（Google）
oauth = OAuth()

def init_oauth(app):
    """OAuth初期化"""
    oauth.init_app(app)
    
    google = oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    return google

@auth_bp.route('/register', methods=['POST'])
def register():
    """ユーザー登録"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'JSONデータが必要です'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'ユーザー名、メールアドレス、パスワードは必須です'}), 400
    
    # パスワードの強度チェック
    if len(password) < 8:
        return jsonify({'error': 'パスワードは8文字以上である必要があります'}), 400
    
    user, error = AuthService.create_user_with_email(username, email, password)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'ユーザーが作成されました。メールアドレスに送信された認証リンクをクリックしてください。',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """ログイン"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'JSONデータが必要です'}), 400
    
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    
    if not all([username_or_email, password]):
        return jsonify({'error': 'ユーザー名/メールアドレスとパスワードは必須です'}), 400
    
    user, error = AuthService.authenticate_user(username_or_email, password)
    
    if error:
        return jsonify({'error': error}), 401
    
    login_user(user)
    
    return jsonify({
        'message': 'ログインしました',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """ログアウト"""
    logout_user()
    return jsonify({'message': 'ログアウトしました'}), 200

@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    """メールアドレス認証"""
    success, message = AuthService.verify_user_email(token)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """パスワード忘れ"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'JSONデータが必要です'}), 400
    
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'メールアドレスは必須です'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        AuthService.send_password_reset_email(user)
    
    # セキュリティのため、ユーザーが存在しなくても同じレスポンスを返す
    return jsonify({
        'message': 'パスワードリセットのメールを送信しました（該当するアカウントが存在する場合）'
    }), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    """パスワードリセット"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'JSONデータが必要です'}), 400
    
    new_password = data.get('password')
    
    if not new_password:
        return jsonify({'error': '新しいパスワードは必須です'}), 400
    
    if len(new_password) < 8:
        return jsonify({'error': 'パスワードは8文字以上である必要があります'}), 400
    
    success, message = AuthService.reset_password(token, new_password)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@auth_bp.route('/google')
def google_auth():
    """Google認証開始"""
    google = oauth.google
    redirect_uri = url_for('auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/google/callback')
def google_callback():
    """Google認証コールバック"""
    google = oauth.google
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        user, error = AuthService.create_or_get_google_user(user_info)
        
        if error:
            return jsonify({'error': error}), 400
        
        login_user(user)
        
        # フロントエンドにリダイレクト
        return redirect(f"{request.host_url}?login=success")
    
    return jsonify({'error': 'Google認証に失敗しました'}), 400

@auth_bp.route('/me')
@login_required
def get_current_user():
    """現在のユーザー情報を取得"""
    return jsonify({'user': current_user.to_dict()}), 200

@auth_bp.route('/resend-verification', methods=['POST'])
@login_required
def resend_verification():
    """認証メールを再送信"""
    if current_user.email_verified:
        return jsonify({'error': 'メールアドレスは既に認証済みです'}), 400
    
    token = AuthService.generate_email_verification_token(current_user.email)
    current_user.email_verification_token = token
    db.session.commit()
    
    AuthService.send_verification_email(current_user, token)
    
    return jsonify({'message': '認証メールを再送信しました'}), 200
