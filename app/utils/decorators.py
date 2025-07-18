# -*- coding: utf-8 -*-
"""
カスタムデコレータ
"""

from functools import wraps
from flask import jsonify
from flask_login import current_user

from app.projects.services import ProjectService


def require_login():
    """API用のログイン要求デコレータ"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'ログインが必要です'}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_project_permission(permission='member'):
    """プロジェクトの権限を要求するデコレータ"""
    def decorator(f):
        @wraps(f)
        def decorated_function(project_id, *args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'ログインが必要です'}), 401
            
            if not ProjectService.check_user_permission(project_id, current_user.id, permission):
                return jsonify({'error': '権限がありません'}), 403
            
            return f(project_id, *args, **kwargs)
        return decorated_function
    return decorator


def require_json():
    """JSONリクエストを要求するデコレータ"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            if not request.is_json:
                return jsonify({'error': 'JSONデータが必要です'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
