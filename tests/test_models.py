# -*- coding: utf-8 -*-
"""
モデル関連のテスト
"""

import pytest
from app.models import db, User, Project, KnowledgeBase


class TestUserModel:
    """ユーザーモデルのテスト"""
    
    def test_create_user(self, app):
        """ユーザー作成テスト"""
        with app.app_context():
            user = User(
                email='model_test@example.com',
                username='modeluser',
                email_verified=True
            )
            user.set_password('testpassword')
            
            assert user.email == 'model_test@example.com'
            assert user.username == 'modeluser'
            assert user.check_password('testpassword')
            assert not user.check_password('wrongpassword')
    
    def test_user_to_dict(self, app, test_user):
        """ユーザーのto_dict メソッドテスト"""
        with app.app_context():
            user_dict = test_user.to_dict()
            
            assert 'id' in user_dict
            assert 'email' in user_dict
            assert 'username' in user_dict
            assert 'password_hash' not in user_dict  # パスワードハッシュは含まれない


class TestProjectModel:
    """プロジェクトモデルのテスト"""
    
    def test_create_project(self, app, test_user):
        """プロジェクト作成テスト"""
        with app.app_context():
            project = Project(
                name='Model Test Project',
                description='Test Description',
                owner_id=test_user.id
            )
            
            assert project.name == 'Model Test Project'
            assert project.description == 'Test Description'
            assert project.owner_id == test_user.id
    
    def test_project_to_dict(self, app, test_project):
        """プロジェクトのto_dict メソッドテスト"""
        with app.app_context():
            # 新しいセッションでプロジェクトを取得（リレーションシップを含む）
            project = db.session.get(Project, test_project.id)
            project_dict = project.to_dict()
            
            assert 'id' in project_dict
            assert 'name' in project_dict
            assert 'description' in project_dict
            assert 'owner_id' in project_dict


class TestKnowledgeBaseModel:
    """ナレッジベースモデルのテスト"""
    
    def test_create_knowledge_base(self, app, test_project, test_user):
        """ナレッジベース作成テスト"""
        with app.app_context():
            # 新しいセッションでプロジェクトとユーザーを取得
            project = db.session.get(Project, test_project.id)
            user = db.session.get(User, test_user.id)
            kb = KnowledgeBase(
                title='Model Test KB',
                content='Test KB Content',
                project_id=project.id,
                created_by_id=user.id
            )
            
            assert kb.title == 'Model Test KB'
            assert kb.content == 'Test KB Content'
            assert kb.project_id == project.id
    
    def test_knowledge_base_to_dict(self, app, test_knowledge_base):
        """ナレッジベースのto_dict メソッドテスト"""
        with app.app_context():
            # 新しいセッションでナレッジベースを取得
            kb = db.session.get(KnowledgeBase, test_knowledge_base.id)
            kb_dict = kb.to_dict()
            
            assert 'id' in kb_dict
            assert 'title' in kb_dict
            assert 'content' in kb_dict
            assert 'project_id' in kb_dict
