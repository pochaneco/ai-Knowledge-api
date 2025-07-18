# -*- coding: utf-8 -*-
"""
ナレッジベースモデル
"""

from datetime import datetime
from sqlalchemy import JSON, Text, Index
from sqlalchemy.sql import func

from . import db


class KnowledgeBase(db.Model):
    """ナレッジベースモデル"""
    __tablename__ = 'knowledge_base'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(Text, nullable=False)
    category = db.Column(db.String(50))
    tags = db.Column(JSON)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # リレーションシップ
    created_by = db.relationship('User', backref='created_knowledge_items')
    
    # インデックス
    __table_args__ = (
        Index('idx_project_id', 'project_id'),
        Index('idx_category', 'category'),
        Index('idx_knowledge_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f'<KnowledgeBase {self.title}>'
    
    def to_dict(self):
        """辞書形式で返す"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.tags,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'created_by_id': self.created_by_id,
            'created_by': self.created_by.username if self.created_by else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
