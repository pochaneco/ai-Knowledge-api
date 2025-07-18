# -*- coding: utf-8 -*-
"""
テストユーティリティ
"""

import pytest
from app import create_app
from app.models import db, User, Project, KnowledgeBase


@pytest.fixture
def app():
    """テスト用アプリケーション"""
    app = create_app('testing')
    
    # Docker環境の場合はMySQLを使用、ローカルの場合はSQLiteを使用
    import os
    if os.environ.get('USE_MYSQL_FOR_TESTING'):
        # Docker環境用：実際のMySQLデータベースを使用
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_user = os.environ.get('DB_USER', 'app_user')
        db_password = os.environ.get('DB_PASSWORD', 'app_password')
        db_name = os.environ.get('DB_NAME', 'test_ai_knowledge_db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}'
    else:
        # ローカル環境用：インメモリSQLite（高速）
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """テストクライアント"""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """テストユーザー"""
    user = None
    with app.app_context():
        user = User(
            email='test@example.com',
            username='testuser',
            email_verified=True
        )
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    # 新しいコンテキストでユーザーを取得
    with app.app_context():
        return db.session.get(User, user_id)


@pytest.fixture
def test_project(app, test_user):
    """テストプロジェクト"""
    with app.app_context():
        # 新しいセッションでユーザーを取得
        user = db.session.get(User, test_user.id)
        project = Project(
            name='Test Project',
            description='Test Description',
            owner_id=user.id
        )
        db.session.add(project)
        db.session.commit()
        
        # オーナーをメンバーとして追加
        project.members.append(user)
        db.session.commit()
        
        project_id = project.id
        
    # 新しいコンテキストでプロジェクトを取得
    with app.app_context():
        return db.session.get(Project, project_id)


@pytest.fixture
def test_knowledge_base(app, test_project, test_user):
    """テストナレッジベース"""
    with app.app_context():
        # 新しいセッションでプロジェクトとユーザーを取得
        project = db.session.get(Project, test_project.id)
        user = db.session.get(User, test_user.id)
        kb = KnowledgeBase(
            title='Test Knowledge Base',
            content='Test KB Description',
            project_id=project.id,
            created_by_id=user.id
        )
        db.session.add(kb)
        db.session.commit()
        kb_id = kb.id
        
    # 新しいコンテキストでナレッジベースを取得
    with app.app_context():
        return db.session.get(KnowledgeBase, kb_id)


@pytest.fixture
def authenticated_client(client, test_user):
    """認証済みクライアント"""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(test_user.id)
        sess['_fresh'] = True
    return client
