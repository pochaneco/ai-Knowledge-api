# -*- coding: utf-8 -*-
"""
プロジェクト API v1
"""

from flask import request, jsonify
from . import api_v1_bp
from ...models import Project
from ...projects.services import ProjectService
from ...utils.decorators import require_project_permission, require_login
from ...utils.logger import get_logger
from app.models import db  # dbを明示的にインポート

logger = get_logger(__name__)


@api_v1_bp.route('/projects', methods=['GET'])
@require_login()
def list_projects():
    """プロジェクト一覧取得"""
    try:
        from flask_login import current_user
        projects = ProjectService.get_user_projects(current_user.id)
        return jsonify({
            'projects': projects  # すでに辞書形式で返されている
        })
    except Exception as e:
        logger.error(f"プロジェクト一覧取得エラー: {str(e)}")
        return jsonify({'error': 'プロジェクト一覧の取得に失敗しました'}), 500


@api_v1_bp.route('/projects', methods=['POST'])
@require_login()
def create_new_project():
    """プロジェクト作成"""
    try:
        from flask_login import current_user
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'プロジェクト名が必要です'}), 400
        
        project = ProjectService.create_project(
            name=name,
            description=description,
            owner_id=current_user.id
        )
        
        return jsonify({
            'project': project.to_dict(),
            'message': 'プロジェクトが作成されました'
        }), 201
    except Exception as e:
        logger.error(f"プロジェクト作成エラー: {str(e)}")
        return jsonify({'error': 'プロジェクトの作成に失敗しました'}), 500


@api_v1_bp.route('/projects/<int:project_id>', methods=['GET'])
@require_project_permission('member')
def get_project_detail(project_id):
    """プロジェクト詳細取得"""
    try:
        project = db.session.get(Project, project_id)  # 修正箇所
        if not project:
            return jsonify({'error': 'プロジェクトが見つかりません'}), 404

        return jsonify({'project': project.to_dict()})
    except Exception as e:
        logger.error(f"プロジェクト詳細取得エラー: {str(e)}")
        return jsonify({'error': 'プロジェクトの取得に失敗しました'}), 500
