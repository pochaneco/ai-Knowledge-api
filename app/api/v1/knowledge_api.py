# -*- coding: utf-8 -*-
"""
ナレッジベース API v1
"""

from flask import request, jsonify
from . import api_v1_bp
from ...knowledge.services import (
    create_knowledge_base, 
    get_knowledge_base, 
    update_knowledge_base, 
    delete_knowledge_base,
    search_knowledge_base,
    get_project_knowledge_bases
)
from ...utils.decorators import require_project_permission, require_login
from ...utils.logger import get_logger

logger = get_logger(__name__)


@api_v1_bp.route('/knowledge', methods=['GET'])
@require_login()
def list_knowledge_bases():
    """ナレッジベース一覧取得"""
    try:
        project_id = request.args.get('project_id', type=int)
        if not project_id:
            return jsonify({'error': 'project_idが必要です'}), 400
        
        knowledge_bases = get_project_knowledge_bases(project_id)
        return jsonify({
            'knowledge_bases': [kb.to_dict() for kb in knowledge_bases]
        })
    except Exception as e:
        logger.error(f"ナレッジベース一覧取得エラー: {str(e)}")
        return jsonify({'error': 'ナレッジベース一覧の取得に失敗しました'}), 500


@api_v1_bp.route('/knowledge', methods=['POST'])
@require_login()
def create_knowledge():
    """ナレッジベース作成"""
    try:
        from flask_login import current_user
        
        data = request.json
        title = data.get('title')
        content = data.get('content', '')
        project_id = data.get('project_id')
        category = data.get('category')
        
        if not title or not project_id:
            return jsonify({'error': 'タイトルとプロジェクトIDが必要です'}), 400
        
        knowledge_base = create_knowledge_base(
            title=title,
            content=content,
            project_id=project_id,
            category=category,
            created_by_id=current_user.id
        )
        
        return jsonify({
            'knowledge_base': knowledge_base.to_dict(),
            'message': 'ナレッジベースが作成されました'
        }), 201
    except Exception as e:
        logger.error(f"ナレッジベース作成エラー: {str(e)}")
        return jsonify({'error': 'ナレッジベースの作成に失敗しました'}), 500


@api_v1_bp.route('/knowledge/<int:kb_id>', methods=['GET'])
@require_login()
def get_knowledge(kb_id):
    """ナレッジベース詳細取得"""
    try:
        knowledge_base = get_knowledge_base(kb_id)
        if not knowledge_base:
            return jsonify({'error': 'ナレッジベースが見つかりません'}), 404
        
        return jsonify({'knowledge_base': knowledge_base.to_dict()})
    except Exception as e:
        logger.error(f"ナレッジベース詳細取得エラー: {str(e)}")
        return jsonify({'error': 'ナレッジベースの取得に失敗しました'}), 500


@api_v1_bp.route('/knowledge/<int:kb_id>', methods=['PUT'])
@require_login()
def update_knowledge(kb_id):
    """ナレッジベース更新"""
    try:
        data = request.json
        knowledge_base = update_knowledge_base(
            kb_id=kb_id,
            name=data.get('name'),
            description=data.get('description')
        )
        
        if not knowledge_base:
            return jsonify({'error': 'ナレッジベースが見つかりません'}), 404
        
        return jsonify({
            'knowledge_base': knowledge_base.to_dict(),
            'message': 'ナレッジベースが更新されました'
        })
    except Exception as e:
        logger.error(f"ナレッジベース更新エラー: {str(e)}")
        return jsonify({'error': 'ナレッジベースの更新に失敗しました'}), 500


@api_v1_bp.route('/knowledge/<int:kb_id>', methods=['DELETE'])
@require_login()
def delete_knowledge(kb_id):
    """ナレッジベース削除"""
    try:
        success = delete_knowledge_base(kb_id)
        if not success:
            return jsonify({'error': 'ナレッジベースが見つかりません'}), 404
        
        return jsonify({'message': 'ナレッジベースが削除されました'})
    except Exception as e:
        logger.error(f"ナレッジベース削除エラー: {str(e)}")
        return jsonify({'error': 'ナレッジベースの削除に失敗しました'}), 500


@api_v1_bp.route('/knowledge/<int:kb_id>/search', methods=['POST'])
@require_login()
def search_knowledge(kb_id):
    """ナレッジベース検索"""
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({'error': '検索クエリが必要です'}), 400
        
        results = search_knowledge_base(kb_id, query)
        return jsonify({'results': results})
    except Exception as e:
        logger.error(f"ナレッジベース検索エラー: {str(e)}")
        return jsonify({'error': '検索に失敗しました'}), 500
