# -*- coding: utf-8 -*-
"""
プロジェクト関連のテスト
"""

import pytest


class TestProjects:
    """プロジェクトテストクラス"""
    
    def test_create_project_success(self, authenticated_client):
        """プロジェクト作成成功テスト"""
        project_data = {
            'name': 'New Project',
            'description': 'New project description'
        }
        
        response = authenticated_client.post('/api/v1/projects', json=project_data)
        assert response.status_code == 201
        assert 'project' in response.json
        assert response.json['project']['name'] == project_data['name']
    
    def test_create_project_missing_name(self, authenticated_client):
        """プロジェクト名なしでの作成テスト"""
        project_data = {
            'description': 'Project without name'
        }
        
        response = authenticated_client.post('/api/v1/projects', json=project_data)
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_get_projects(self, authenticated_client):
        """プロジェクト一覧取得テスト"""
        response = authenticated_client.get('/api/v1/projects')
        assert response.status_code == 200
        assert 'projects' in response.json
        assert isinstance(response.json['projects'], list)
    
    def test_get_project_detail(self, authenticated_client, test_project):
        """プロジェクト詳細取得テスト"""
        response = authenticated_client.get(f'/api/v1/projects/{test_project.id}')
        assert response.status_code == 200
        assert 'project' in response.json
        assert response.json['project']['id'] == test_project.id
    
    def test_unauthorized_access(self, client):
        """未認証でのアクセステスト"""
        response = client.get('/api/v1/projects')
        assert response.status_code == 401
        assert 'error' in response.json
