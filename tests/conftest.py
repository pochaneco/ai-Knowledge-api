# -*- coding: utf-8 -*-
"""
テストユーティリティ
"""

import pytest
from app import create_app
from app.models import db, User, Project, KnowledgeBase


@pytest.fixture(scope='function')
def app():
    """テスト用アプリケーション"""
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # CSRFを無効化
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """テストクライアント"""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """テストユーザー"""
    with app.app_context():
        user = User(
            email='test@example.com',
            username='testuser',
            email_verified=True
        )
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()
        
        # セッションから切り離して、IDだけを保持
        user_id = user.id
        db.session.expunge(user)
        
        # 新しいインスタンスとして返す
        fresh_user = db.session.get(User, user_id)
        return fresh_user


@pytest.fixture
def test_project(app, test_user):
    """テストプロジェクト"""
    with app.app_context():
        from app.projects.services import ProjectService
        
        # 新しいセッションでユーザーを取得
        user = db.session.get(User, test_user.id)
        
        # ProjectServiceを使用してプロジェクトを作成
        project = ProjectService.create_project(
            name='Test Project',
            description='Test Description',
            owner_id=user.id
        )
        
        # セッションから切り離して、IDだけを保持
        project_id = project.id
        db.session.expunge(project)
        
        # 新しいインスタンスとして返す
        fresh_project = db.session.get(Project, project_id)
        return fresh_project


@pytest.fixture
def test_knowledge_base(app, test_project):
    """テストナレッジベース"""
    with app.app_context():
        # 新しいセッションでプロジェクトを取得
        project = db.session.get(Project, test_project.id)
        
        kb = KnowledgeBase(
            title='Test Knowledge Base',
            content='Test KB Content',
            category='test',
            project_id=project.id,
            created_by_id=project.owner_id
        )
        db.session.add(kb)
        db.session.commit()
        
        # セッションから切り離して、IDだけを保持
        kb_id = kb.id
        db.session.expunge(kb)
        
        # 新しいインスタンスとして返す
        fresh_kb = db.session.get(KnowledgeBase, kb_id)
        return fresh_kb


@pytest.fixture
def authenticated_client(client, test_user):
    """認証済みクライアント"""
    # APIを使ってログイン
    response = client.post('/api/v1/auth/login', json={
        'email': test_user.email,
        'password': 'testpassword123'
    })
    assert response.status_code == 200
    return client
