# -*- coding: utf-8 -*-
"""
認証関連ビュー（Webページ）
"""

from flask import Blueprint
from app.inertia_config import render


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login')
def login():
    """ログインページ"""
    return render('auth/Login')


@auth_bp.route('/register')
def register():
    """ユーザー登録ページ"""
    return render('auth/Register')


@auth_bp.route('/forgot-password')
def forgot_password():
    """パスワードリセットページ"""
    return render('auth/ForgotPassword')


@auth_bp.route('/reset-password/<token>')
def reset_password(token):
    """パスワードリセット実行ページ"""
    return render('auth/ResetPassword', {'token': token})


@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    """メールアドレス認証ページ"""
    return render('auth/VerifyEmail', {'token': token})
