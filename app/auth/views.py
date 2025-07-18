# -*- coding: utf-8 -*-
"""
認証関連ビュー（Webページ）
"""

from flask import Blueprint, render_template


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login')
def login():
    """ログインページ"""
    return render_template('auth/login.html')


@auth_bp.route('/register')
def register():
    """ユーザー登録ページ"""
    return render_template('auth/register.html')


@auth_bp.route('/forgot-password')
def forgot_password():
    """パスワードリセットページ"""
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>')
def reset_password(token):
    """パスワードリセット実行ページ"""
    return render_template('auth/reset_password.html', token=token)


@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    """メールアドレス認証ページ"""
    return render_template('auth/verify_email.html', token=token)
