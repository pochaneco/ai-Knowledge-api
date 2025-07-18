# -*- coding: utf-8 -*-
"""
バリデータ関数
"""

import re
from email_validator import validate_email, EmailNotValidError


def is_valid_email(email):
    """メールアドレスの妥当性をチェック"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def is_strong_password(password):
    """パスワードの強度をチェック"""
    if len(password) < 8:
        return False, "パスワードは8文字以上である必要があります"
    
    if not re.search(r"[a-z]", password):
        return False, "パスワードには小文字を含める必要があります"
    
    if not re.search(r"[A-Z]", password):
        return False, "パスワードには大文字を含める必要があります"
    
    if not re.search(r"\d", password):
        return False, "パスワードには数字を含める必要があります"
    
    return True, "有効なパスワードです"


def is_valid_username(username):
    """ユーザー名の妥当性をチェック"""
    if len(username) < 3:
        return False, "ユーザー名は3文字以上である必要があります"
    
    if len(username) > 50:
        return False, "ユーザー名は50文字以下である必要があります"
    
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "ユーザー名には英数字とアンダースコアのみ使用できます"
    
    return True, "有効なユーザー名です"


def is_valid_project_name(name):
    """プロジェクト名の妥当性をチェック"""
    if len(name) < 1:
        return False, "プロジェクト名は必須です"
    
    if len(name) > 100:
        return False, "プロジェクト名は100文字以下である必要があります"
    
    return True, "有効なプロジェクト名です"
