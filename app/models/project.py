# -*- coding: utf-8 -*-
"""
プロジェクト関連モデル
"""

from datetime import datetime
from sqlalchemy import JSON, Text, Index, Table
from sqlalchemy.sql import func

from . import db


# プロジェクトメンバーシップの中間テーブル
project_members = Table(
    'project_members',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('role', db.String(20), default='member'),  # owner, admin, member
    db.Column('joined_at', db.DateTime, default=func.current_timestamp())
)


class Project(db.Model):
    """プロジェクトモデル"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_private = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # リレーションシップ
    owner = db.relationship('User', foreign_keys=[owner_id], backref='owned_projects')
    members = db.relationship('User', secondary=project_members, back_populates='projects')
    knowledge_items = db.relationship('KnowledgeBase', backref='project', lazy=True, cascade='all, delete-orphan')
    invitations = db.relationship('ProjectInvitation', backref='project', lazy=True, cascade='all, delete-orphan')
    
    # インデックス
    __table_args__ = (
        Index('idx_owner_id', 'owner_id'),
        Index('idx_projects_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f'<Project {self.name}>'
    
    def to_dict(self):
        """辞書形式で返す"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'owner': self.owner.username if self.owner else None,
            'is_private': self.is_private,
            'member_count': len(self.members),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ProjectInvitation(db.Model):
    """プロジェクト招待モデル"""
    __tablename__ = 'project_invitations'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    invited_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, expired
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    
    # リレーションシップ
    invited_by = db.relationship('User', backref='sent_invitations')
    
    # インデックス
    __table_args__ = (
        Index('idx_email', 'email'),
        Index('idx_token', 'token'),
        Index('idx_expires_at', 'expires_at'),
    )
    
    def __repr__(self):
        return f'<ProjectInvitation {self.email} to {self.project.name}>'
    
    def to_dict(self):
        """辞書形式で返す"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'email': self.email,
            'invited_by': self.invited_by.username if self.invited_by else None,
            'status': self.status,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
