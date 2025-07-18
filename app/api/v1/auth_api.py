# -*- coding: utf-8 -*-
"""
認証 API v1
"""

from flask import request, jsonify
from . import api_v1_bp
from ...auth.services import AuthService
from ...utils.logger import get_logger
from ...utils.decorators import require_login
from ...utils.validators import is_valid_email, is_valid_username

logger = get_logger(__name__)


@api_v1_bp.route('/auth/register', methods=['POST'])
def register():
    """ユーザー登録API"""
    try:
        # Content-Typeチェック
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.json
        if not data:
            return jsonify({'error': 'JSONデータが必要です'}), 400
            
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        
        if not all([email, password, username]):
            return jsonify({'error': 'すべての項目が必要です'}), 400
        
        # バリデーション
        if not is_valid_email(email):
            return jsonify({'error': '有効なメールアドレスを入力してください'}), 400
        
        is_valid, username_error = is_valid_username(username)
        if not is_valid:
            return jsonify({'error': username_error}), 400
        
        user, error = AuthService.create_user_with_email(username, email, password)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'user': user.to_dict(),
            'message': 'ユーザーが作成されました。メール認証を行ってください。'
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"ユーザー登録エラー: {str(e)}")
        return jsonify({'error': 'ユーザー登録に失敗しました'}), 500


@api_v1_bp.route('/auth/login', methods=['POST'])
def login():
    """ログインAPI"""
    try:
        from flask_login import login_user
        
        # Content-Typeチェック
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.json
        if not data:
            return jsonify({'error': 'JSONデータが必要です'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'メールアドレスとパスワードが必要です'}), 400
        
        user, error = AuthService.authenticate_user(email, password)
        if error:
            return jsonify({'error': error}), 401
        
        # Flask-Loginでユーザーをログイン状態にする
        login_user(user)
        
        return jsonify({
            'user': user.to_dict(),
            'message': 'ログインしました'
        })
    except Exception as e:
        logger.error(f"ログインエラー: {str(e)}")
        return jsonify({'error': 'ログインに失敗しました'}), 500


@api_v1_bp.route('/auth/logout', methods=['POST'])
def logout():
    """ログアウトAPI"""
    try:
        from flask_login import logout_user, current_user
        
        if current_user.is_authenticated:
            logout_user()
        
        return jsonify({'message': 'ログアウトしました'})
    except Exception as e:
        logger.error(f"ログアウトエラー: {str(e)}")
        return jsonify({'error': 'ログアウトに失敗しました'}), 500


@api_v1_bp.route('/auth/me', methods=['GET'])
@require_login()
def get_current_user():
    """現在のユーザー情報取得API"""
    try:
        from flask_login import current_user
        return jsonify({'user': current_user.to_dict()})
    except Exception as e:
        logger.error(f"ユーザー情報取得エラー: {str(e)}")
        return jsonify({'error': 'ユーザー情報の取得に失敗しました'}), 500
