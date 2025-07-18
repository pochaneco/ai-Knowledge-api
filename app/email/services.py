#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
メールサービス
Flask-Mailを使用したメール送信機能
"""

from flask_mail import Mail

# メールインスタンス
mail = Mail()

def init_mail(app):
    """メールサービスを初期化"""
    mail.init_app(app)
