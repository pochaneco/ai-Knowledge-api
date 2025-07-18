# -*- coding: utf-8 -*-
"""
データベースモデルの初期化
"""

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemyインスタンス
db = SQLAlchemy()

# モデルをインポート
from .user import User
from .project import Project, ProjectInvitation, project_members
from .knowledge import KnowledgeBase
from .search_log import SearchLog

__all__ = [
    'db',
    'User',
    'Project',
    'ProjectInvitation', 
    'project_members',
    'KnowledgeBase',
    'SearchLog'
]
