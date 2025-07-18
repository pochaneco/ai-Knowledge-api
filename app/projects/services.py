#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
プロジェクトサービス
プロジェクトの作成、管理、招待機能を提供
"""

import secrets
from datetime import datetime, timedelta
from flask import current_app, url_for
from flask_mail import Message
from ..models import db, Project, User, ProjectInvitation, project_members
from ..email.services import mail

class ProjectService:
    """プロジェクトサービスクラス"""
    
    @staticmethod
    def create_project(name, description, owner_id, is_private=True):
        """プロジェクトを作成"""
        project = Project(
            name=name,
            description=description,
            owner_id=owner_id,
            is_private=is_private
        )
        
        db.session.add(project)
        db.session.flush()  # IDを取得するためにflush
        
        # オーナーをメンバーとして追加
        ProjectService.add_member(project.id, owner_id, 'owner')
        
        db.session.commit()
        return project
    
    @staticmethod
    def add_member(project_id, user_id, role='member'):
        """プロジェクトにメンバーを追加"""
        # 既存メンバーかチェック
        existing = db.session.execute(
            project_members.select().where(
                (project_members.c.project_id == project_id) &
                (project_members.c.user_id == user_id)
            )
        ).first()
        
        if existing:
            return False, "ユーザーは既にプロジェクトのメンバーです"
        
        # メンバーを追加
        db.session.execute(
            project_members.insert().values(
                project_id=project_id,
                user_id=user_id,
                role=role
            )
        )
        db.session.commit()
        return True, "メンバーが追加されました"
    
    @staticmethod
    def invite_user(project_id, email, invited_by_id):
        """ユーザーをプロジェクトに招待"""
        project = Project.query.get(project_id)
        if not project:
            return None, "プロジェクトが見つかりません"
        
        # 既存の招待をチェック
        existing_invitation = ProjectInvitation.query.filter_by(
            project_id=project_id,
            email=email,
            status='pending'
        ).first()
        
        if existing_invitation:
            return None, "このメールアドレスには既に招待が送信されています"
        
        # 既にプロジェクトメンバーかチェック
        user = User.query.filter_by(email=email).first()
        if user:
            is_member = db.session.execute(
                project_members.select().where(
                    (project_members.c.project_id == project_id) &
                    (project_members.c.user_id == user.id)
                )
            ).first()
            
            if is_member:
                return None, "このユーザーは既にプロジェクトのメンバーです"
        
        # 招待を作成
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=7)  # 7日間有効
        
        invitation = ProjectInvitation(
            project_id=project_id,
            email=email,
            invited_by_id=invited_by_id,
            token=token,
            expires_at=expires_at
        )
        
        db.session.add(invitation)
        db.session.commit()
        
        # 招待メールを送信
        ProjectService.send_invitation_email(invitation)
        
        return invitation, None
    
    @staticmethod
    def send_invitation_email(invitation):
        """招待メールを送信"""
        invitation_url = url_for('project.accept_invitation', token=invitation.token, _external=True)
        
        msg = Message(
            subject=f'【AI Knowledge API】プロジェクト「{invitation.project.name}」への招待',
            recipients=[invitation.email],
            html=f'''
            <h2>プロジェクトへの招待</h2>
            <p>こんにちは</p>
            <p>{invitation.invited_by.username} さんから、プロジェクト「{invitation.project.name}」への招待が届いています。</p>
            <p><strong>プロジェクト説明:</strong></p>
            <p>{invitation.project.description or "説明なし"}</p>
            <p>以下のリンクをクリックして招待を受け入れてください：</p>
            <p><a href="{invitation_url}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">招待を受け入れる</a></p>
            <p>この招待は{invitation.expires_at.strftime('%Y年%m月%d日')}まで有効です。</p>
            <p>もしこの招待に心当たりがない場合は、このメールを無視してください。</p>
            '''
        )
        mail.send(msg)
    
    @staticmethod
    def accept_invitation(token):
        """招待を受け入れる"""
        invitation = ProjectInvitation.query.filter_by(token=token, status='pending').first()
        
        if not invitation:
            return False, "招待が見つからないか、既に処理済みです"
        
        if invitation.expires_at < datetime.utcnow():
            invitation.status = 'expired'
            db.session.commit()
            return False, "招待の有効期限が切れています"
        
        # ユーザーを取得または作成
        user = User.query.filter_by(email=invitation.email).first()
        if not user:
            return False, "アカウントを作成してからもう一度お試しください"
        
        # プロジェクトにメンバーとして追加
        success, message = ProjectService.add_member(invitation.project_id, user.id, 'member')
        if not success:
            return False, message
        
        # 招待のステータスを更新
        invitation.status = 'accepted'
        db.session.commit()
        
        return True, "プロジェクトに参加しました"
    
    @staticmethod
    def get_user_projects(user_id):
        """ユーザーが参加しているプロジェクト一覧を取得"""
        projects = db.session.query(Project, project_members.c.role).join(
            project_members,
            Project.id == project_members.c.project_id
        ).filter(
            project_members.c.user_id == user_id
        ).all()
        
        return [
            {
                **project.to_dict(),
                'user_role': role
            }
            for project, role in projects
        ]
    
    @staticmethod
    def check_user_permission(project_id, user_id, required_role='member'):
        """ユーザーのプロジェクト権限をチェック"""
        membership = db.session.execute(
            project_members.select().where(
                (project_members.c.project_id == project_id) &
                (project_members.c.user_id == user_id)
            )
        ).first()
        
        if not membership:
            return False
        
        role_hierarchy = {'member': 1, 'admin': 2, 'owner': 3}
        user_level = role_hierarchy.get(membership.role, 0)
        required_level = role_hierarchy.get(required_role, 1)
        
        return user_level >= required_level
    
    @staticmethod
    def remove_member(project_id, user_id, removed_by_id):
        """プロジェクトからメンバーを削除"""
        project = Project.query.get(project_id)
        if not project:
            return False, "プロジェクトが見つかりません"
        
        # オーナーは削除できない
        if project.owner_id == user_id:
            return False, "プロジェクトオーナーは削除できません"
        
        # 権限チェック（オーナーまたは管理者のみ）
        if not ProjectService.check_user_permission(project_id, removed_by_id, 'admin'):
            return False, "権限がありません"
        
        # メンバーを削除
        db.session.execute(
            project_members.delete().where(
                (project_members.c.project_id == project_id) &
                (project_members.c.user_id == user_id)
            )
        )
        db.session.commit()
        
        return True, "メンバーが削除されました"
