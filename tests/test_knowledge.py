# -*- coding: utf-8 -*-
"""
ナレッジベース関連のテスト
"""

import pytest


class TestKnowledge:
    """ナレッジベーステストクラス"""
    
    def test_create_knowledge_base_success(self, authenticated_client, test_project):
        """ナレッジベース作成成功テスト"""
        kb_data = {
            'title': 'New Knowledge Base',
            'content': 'New KB content',
            'project_id': test_project.id,
            'category': 'test'
        }
        
        response = authenticated_client.post('/api/v1/knowledge', json=kb_data)
        assert response.status_code == 201
        assert 'knowledge_base' in response.json
        assert response.json['knowledge_base']['title'] == kb_data['title']
    
    def test_create_knowledge_base_missing_name(self, authenticated_client, test_project):
        """ナレッジベースタイトルなしでの作成テスト"""
        kb_data = {
            'content': 'KB without title',
            'project_id': test_project.id
        }
        
        response = authenticated_client.post('/api/v1/knowledge', json=kb_data)
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_get_knowledge_bases(self, authenticated_client, test_project):
        """ナレッジベース一覧取得テスト"""
        response = authenticated_client.get(f'/api/v1/knowledge?project_id={test_project.id}')
        assert response.status_code == 200
        assert 'knowledge_bases' in response.json
        assert isinstance(response.json['knowledge_bases'], list)
    
    def test_get_knowledge_base_detail(self, authenticated_client, test_knowledge_base):
        """ナレッジベース詳細取得テスト"""
        response = authenticated_client.get(f'/api/v1/knowledge/{test_knowledge_base.id}')
        assert response.status_code == 200
        assert 'knowledge_base' in response.json
        assert response.json['knowledge_base']['id'] == test_knowledge_base.id
    
    def test_search_knowledge_base(self, authenticated_client, test_knowledge_base):
        """ナレッジベース検索テスト"""
        search_data = {
            'query': 'test search'
        }
        
        response = authenticated_client.post(f'/api/v1/knowledge/{test_knowledge_base.id}/search', json=search_data)
        assert response.status_code == 200
        assert 'results' in response.json
    
    def test_unauthorized_access(self, client, test_project):
        """未認証でのアクセステスト"""
        response = client.get(f'/api/v1/knowledge?project_id={test_project.id}')
        assert response.status_code == 401
        assert 'error' in response.json
