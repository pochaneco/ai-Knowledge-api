# -*- coding: utf-8 -*-
"""
統合テスト
"""

import pytest


class TestIntegration:
    """統合テストクラス"""
    
    def test_full_workflow(self, client):
        """完全なワークフローテスト: ユーザー登録 → ログイン → プロジェクト作成 → ナレッジベース作成"""
        
        # 1. ユーザー登録
        user_data = {
            'email': 'workflow@example.com',
            'password': 'password123',
            'username': 'workflowuser'
        }
        
        response = client.post('/api/v1/auth/register', json=user_data)
        assert response.status_code == 201
        
        # 2. ログイン
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        assert response.status_code == 200
        
        # 3. プロジェクト作成
        project_data = {
            'name': 'Workflow Project',
            'description': 'Project for workflow test'
        }
        
        response = client.post('/api/v1/projects', json=project_data)
        assert response.status_code == 201
        project_id = response.json['project']['id']
        
        # 4. ナレッジベース作成
        kb_data = {
            'title': 'Workflow KB',
            'content': 'KB content for workflow test',
            'project_id': project_id,
            'category': 'test'
        }
        
        response = client.post('/api/v1/knowledge', json=kb_data)
        assert response.status_code == 201
        
        # 5. プロジェクト一覧取得
        response = client.get('/api/v1/projects')
        assert response.status_code == 200
        assert len(response.json['projects']) == 1
        
        # 6. ナレッジベース一覧取得
        response = client.get(f'/api/v1/knowledge?project_id={project_id}')
        assert response.status_code == 200
        assert len(response.json['knowledge_bases']) == 1
        
        # 7. ログアウト
        response = client.post('/api/v1/auth/logout')
        assert response.status_code == 200
    
    def test_project_permission_workflow(self, client):
        """プロジェクト権限ワークフローテスト"""
        
        # オーナーユーザー作成とログイン
        owner_data = {
            'email': 'owner@example.com',
            'password': 'password123',
            'username': 'owner'
        }
        
        client.post('/api/v1/auth/register', json=owner_data)
        client.post('/api/v1/auth/login', json={
            'email': owner_data['email'],
            'password': owner_data['password']
        })
        
        # プロジェクト作成
        project_data = {
            'name': 'Permission Test Project',
            'description': 'Project for permission test'
        }
        
        response = client.post('/api/v1/projects', json=project_data)
        assert response.status_code == 201
        project_id = response.json['project']['id']
        
        # プロジェクト詳細取得（オーナーとして）
        response = client.get(f'/api/v1/projects/{project_id}')
        assert response.status_code == 200
        
        # ログアウト
        client.post('/api/v1/auth/logout')
        
        # 別のユーザーでログイン
        member_data = {
            'email': 'member@example.com',
            'password': 'password123',
            'username': 'member'
        }
        
        client.post('/api/v1/auth/register', json=member_data)
        client.post('/api/v1/auth/login', json={
            'email': member_data['email'],
            'password': member_data['password']
        })
        
        # 他人のプロジェクトへのアクセス（権限なし）
        response = client.get(f'/api/v1/projects/{project_id}')
        assert response.status_code == 403
    
    def test_error_handling_workflow(self, client):
        """エラーハンドリングワークフローテスト"""
        
        # 1. 存在しないエンドポイントへのアクセス
        response = client.get('/api/v1/nonexistent')
        assert response.status_code == 404
        
        # 2. 不正なリクエストデータ（非JSON）
        response = client.post('/api/v1/auth/register', 
                             data='invalid data',
                             content_type='text/plain')
        assert response.status_code == 400
        
        # 3. 必須フィールド不足
        response = client.post('/api/v1/auth/register', json={})
        assert response.status_code == 400
        
        # 4. 未認証でのAPIアクセス
        response = client.get('/api/v1/projects')
        assert response.status_code == 401
