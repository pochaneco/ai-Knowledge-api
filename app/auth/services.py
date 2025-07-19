#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
認証サービス
ユーザー登録、ログイン、メール認証などの機能を提供
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from ..models import db, User, ProjectInvitation
from ..email.services import mail

class AuthService:
    """認証サービスクラス"""
    
    @staticmethod
    def generate_verification_token():
        """メール認証用トークンを生成"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_email_verification_token(email):
        """メールアドレス検証用の署名付きトークンを生成"""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt='email-verification')
    
    @staticmethod
    def verify_email_token(token, expiration=3600):
        """メール認証トークンを検証（デフォルト1時間有効）"""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='email-verification', max_age=expiration)
            return email
        except (SignatureExpired, BadSignature):
            return None
    
    @staticmethod
    def create_user_with_email(username, email, password=None, google_id=None):
        """ユーザーを作成してメール認証を送信"""
        from flask import current_app
        
        # 既存ユーザーチェック
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return None, "ユーザー名またはメールアドレスが既に使用されています"
        
        # テスト環境では自動認証
        is_testing = current_app.config.get('TESTING', False)
        
        # ユーザー作成
        user = User(
            username=username,
            email=email,
            google_id=google_id,
            email_verified=True if (google_id or is_testing) else False
        )
        
        if password:
            user.set_password(password)
        
        # メール認証トークン生成（テスト環境以外）
        if not google_id and not is_testing:
            token = AuthService.generate_email_verification_token(email)
            user.email_verification_token = token
        
        db.session.add(user)
        db.session.commit()
        
        # メール認証送信（Googleログイン以外、テスト環境以外）
        if not google_id and not is_testing:
            AuthService.send_verification_email(user, token)
        
        return user, None
    
    @staticmethod
    def send_verification_email(user, token):
        """認証メールを送信"""
        verification_url = url_for('auth.verify_email', token=token, _external=True)
        
        msg = Message(
            subject='【Vidays】メールアドレスの認証',
            recipients=[user.email],
            html=f'''
            <h2>メールアドレスの認証</h2>
            <p>こんにちは {user.username} さん</p>
            <p>Vidaysへのご登録ありがとうございます。</p>
            <p>以下のリンクをクリックしてメールアドレスを認証してください：</p>
            <p><a href="{verification_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">メールアドレスを認証する</a></p>
            <p>このリンクは1時間で有効期限が切れます。</p>
            <p>もしこのメールに心当たりがない場合は、このメールを無視してください。</p>
            '''
        )
        mail.send(msg)
    
    @staticmethod
    def verify_user_email(token):
        """メールアドレスを認証"""
        email = AuthService.verify_email_token(token)
        if not email:
            return False, "認証リンクが無効または期限切れです"
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return False, "ユーザーが見つかりません"
        
        if user.email_verified:
            return True, "メールアドレスは既に認証済みです"
        
        user.email_verified = True
        user.email_verification_token = None
        db.session.commit()
        
        return True, "メールアドレスが正常に認証されました"
    
    @staticmethod
    def authenticate_user(username_or_email, password):
        """ユーザー認証"""
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        
        if not user or not user.check_password(password):
            return None, "ユーザー名/メールアドレスまたはパスワードが正しくありません"
        
        if not user.email_verified:
            return None, "メールアドレスが認証されていません"
        
        if not user.is_active:
            return None, "アカウントが無効化されています"
        
        return user, None
    
    @staticmethod
    def create_or_get_google_user(google_user_info):
        """Google認証でユーザーを作成または取得"""
        google_id = google_user_info.get('sub')
        email = google_user_info.get('email')
        name = google_user_info.get('name', email.split('@')[0])
        
        # Google IDで既存ユーザーを検索
        user = User.query.filter_by(google_id=google_id).first()
        if user:
            return user, None
        
        # メールアドレスで既存ユーザーを検索
        user = User.query.filter_by(email=email).first()
        if user:
            # 既存ユーザーにGoogle IDを追加
            user.google_id = google_id
            user.email_verified = True
            db.session.commit()
            return user, None
        
        # 新規ユーザーを作成
        # ユーザー名の重複チェック
        username = name
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{name}_{counter}"
            counter += 1
        
        return AuthService.create_user_with_email(username, email, google_id=google_id)
    
    @staticmethod
    def send_password_reset_email(user):
        """パスワードリセットメールを送信"""
        token = AuthService.generate_email_verification_token(user.email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        
        msg = Message(
            subject='【Vidays】パスワードリセット',
            recipients=[user.email],
            html=f'''
            <h2>パスワードリセット</h2>
            <p>こんにちは {user.username} さん</p>
            <p>パスワードリセットのリクエストを受け付けました。</p>
            <p>以下のリンクをクリックして新しいパスワードを設定してください：</p>
            <p><a href="{reset_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">パスワードをリセットする</a></p>
            <p>このリンクは1時間で有効期限が切れます。</p>
            <p>もしこのリクエストに心当たりがない場合は、このメールを無視してください。</p>
            '''
        )
        mail.send(msg)
    
    @staticmethod
    def reset_password(token, new_password):
        """パスワードをリセット"""
        email = AuthService.verify_email_token(token)
        if not email:
            return False, "リセットリンクが無効または期限切れです"
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return False, "ユーザーが見つかりません"
        
        user.set_password(new_password)
        db.session.commit()
        
        return True, "パスワードが正常にリセットされました"
