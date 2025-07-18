# -*- coding: utf-8 -*-
"""
検索ログモデル
"""

from datetime import datetime
from sqlalchemy import Index
from sqlalchemy.sql import func

from . import db


class SearchLog(db.Model):
    """検索ログモデル"""
    __tablename__ = 'search_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    query_text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    results_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    
    # インデックス
    __table_args__ = (
        Index('idx_search_logs_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f'<SearchLog {self.query_text[:50]}>'
    
    def to_dict(self):
        """辞書形式で返す"""
        return {
            'id': self.id,
            'query_text': self.query_text,
            'user_id': self.user_id,
            'results_count': self.results_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
