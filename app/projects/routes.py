#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
プロジェクト関連のBlueprint
プロジェクトの作成、管理、招待などのエンドポイント
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import db, Project, ProjectInvitation, KnowledgeBase, project_members
from .services import ProjectService

project_bp = Blueprint('project', __name__, url_prefix='/projects')

@project_bp.route('', methods=['GET'])
@login_required
def get_projects():
    """ユーザーのプロジェクト一覧を取得"""
    projects = ProjectService.get_user_projects(current_user.id)
    return jsonify({'projects': projects}), 200

@project_bp.route('', methods=['POST'])
@login_required
def create_project():
    """プロジェクトを作成"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'JSONデータが必要です'}), 400
    
    name = data.get('name')
    description = data.get('description', '')
    is_private = data.get('is_private', True)
    
    if not name:
        return jsonify({'error': 'プロジェクト名は必須です'}), 400
    
    project = ProjectService.create_project(name, description, current_user.id, is_private)
    
    return jsonify({
        'message': 'プロジェクトが作成されました',
        'project': project.to_dict()
    }), 201

@project_bp.route('/<int:project_id>')
@login_required
def get_project(project_id):
    """プロジェクト詳細を取得"""
    if not ProjectService.check_user_permission(project_id, current_user.id):
        return jsonify({'error': 'このプロジェクトにアクセスする権限がありません'}), 403
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'プロジェクトが見つかりません'}), 404
    
    return jsonify({'project': project.to_dict()}), 200

@project_bp.route('/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    """プロジェクトを更新"""
    if not ProjectService.check_user_permission(project_id, current_user.id, 'admin'):
        return jsonify({'error': 'プロジェクトを編集する権限がありません'}), 403
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'プロジェクトが見つかりません'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSONデータが必要です'}), 400
    
    # 更新可能なフィールド
    if 'name' in data:
        project.name = data['name']
    if 'description' in data:
        project.description = data['description']
    if 'is_private' in data:
        project.is_private = data['is_private']
    
    db.session.commit()
    
    return jsonify({
        'message': 'プロジェクトが更新されました',
        'project': project.to_dict()
    }), 200

@project_bp.route('/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    """プロジェクトを削除"""
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'プロジェクトが見つかりません'}), 404
    
    if project.owner_id != current_user.id:
        return jsonify({'error': 'プロジェクトを削除する権限がありません'}), 403
    
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({'message': 'プロジェクトが削除されました'}), 200

@project_bp.route('/<int:project_id>/invite', methods=['POST'])
@login_required
def invite_user(project_id):
    """ユーザーをプロジェクトに招待"""
    if not ProjectService.check_user_permission(project_id, current_user.id, 'admin'):
        return jsonify({'error': 'ユーザーを招待する権限がありません'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSONデータが必要です'}), 400
    
    email = data.get('email')
    if not email:
        return jsonify({'error': 'メールアドレスは必須です'}), 400
    
    invitation, error = ProjectService.invite_user(project_id, email, current_user.id)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': '招待を送信しました',
        'invitation': invitation.to_dict()
    }), 201

@project_bp.route('/invitations/<token>/accept')
def accept_invitation(token):
    """招待を受け入れる"""
    success, message = ProjectService.accept_invitation(token)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@project_bp.route('/<int:project_id>/members')
@login_required
def get_project_members(project_id):
    """プロジェクトメンバー一覧を取得"""
    if not ProjectService.check_user_permission(project_id, current_user.id):
        return jsonify({'error': 'このプロジェクトにアクセスする権限がありません'}), 403
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'プロジェクトが見つかりません'}), 404
    
    members = []
    for member in project.members:
        # メンバーシップ情報を取得
        membership = db.session.execute(
            project_members.select().where(
                (project_members.c.project_id == project_id) &
                (project_members.c.user_id == member.id)
            )
        ).first()
        
        member_info = member.to_dict()
        member_info['role'] = membership.role if membership else 'member'
        member_info['joined_at'] = membership.joined_at.isoformat() if membership and membership.joined_at else None
        members.append(member_info)
    
    return jsonify({'members': members}), 200

@project_bp.route('/<int:project_id>/members/<int:user_id>', methods=['DELETE'])
@login_required
def remove_member(project_id, user_id):
    """プロジェクトからメンバーを削除"""
    success, message = ProjectService.remove_member(project_id, user_id, current_user.id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@project_bp.route('/<int:project_id>/knowledge')
@login_required
def get_project_knowledge(project_id):
    """プロジェクトのナレッジベース一覧を取得"""
    if not ProjectService.check_user_permission(project_id, current_user.id):
        return jsonify({'error': 'このプロジェクトにアクセスする権限がありません'}), 403
    
    knowledge_items = KnowledgeBase.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'knowledge_items': [item.to_dict() for item in knowledge_items]
    }), 200

@project_bp.route('/<int:project_id>/invitations')
@login_required
def get_project_invitations(project_id):
    """プロジェクトの招待一覧を取得"""
    if not ProjectService.check_user_permission(project_id, current_user.id, 'admin'):
        return jsonify({'error': '招待を確認する権限がありません'}), 403
    
    invitations = ProjectInvitation.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'invitations': [inv.to_dict() for inv in invitations]
    }), 200
