# -*- coding: utf-8 -*-
"""
認証関連のテスト
"""

import pytest


class TestAuth:
    """認証テストクラス"""
    
    def test_register_success(self, client):
        """ユーザー登録成功テスト"""
        user_data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'username': 'newuser'
        }
        
        response = client.post('/api/v1/auth/register', json=user_data)
        assert response.status_code == 201
        assert 'user' in response.json
        assert response.json['user']['email'] == user_data['email']
    
    def test_register_invalid_email(self, client):
        """無効なメールアドレスでの登録テスト"""
        user_data = {
            'email': 'invalid-email',
            'password': 'password123',
            'username': 'testuser'
        }
        
        response = client.post('/api/v1/auth/register', json=user_data)
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_register_duplicate_email(self, client):
        """重複メールアドレスでの登録テスト"""
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'username': 'testuser'
        }
        
        # 最初の登録
        client.post('/api/v1/auth/register', json=user_data)
        
        # 重複登録
        response = client.post('/api/v1/auth/register', json=user_data)
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_login_success(self, client):
        """ログイン成功テスト"""
        # ユーザー登録
        user_data = {
            'email': 'logintest@example.com',
            'password': 'password123',
            'username': 'loginuser'
        }
        client.post('/api/v1/auth/register', json=user_data)
        
        # ログイン
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response = client.post('/api/v1/auth/login', json=login_data)
        assert response.status_code == 200
        assert 'message' in response.json
    
    def test_login_invalid_credentials(self, client):
        """無効な認証情報でのログインテスト"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        assert response.status_code == 401
        assert 'error' in response.json
    
    def test_logout_success(self, client):
        """ログアウト成功テスト"""
        # ユーザー登録とログイン
        user_data = {
            'email': 'logouttest@example.com',
            'password': 'password123',
            'username': 'logoutuser'
        }
        client.post('/api/v1/auth/register', json=user_data)
        client.post('/api/v1/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        
        # ログアウト
        response = client.post('/api/v1/auth/logout')
        assert response.status_code == 200
        assert 'message' in response.json
