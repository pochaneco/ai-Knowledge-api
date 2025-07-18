# -*- coding: utf-8 -*-
"""
ナレッジベースサービス
"""

from sqlalchemy.exc import SQLAlchemyError
from ..models import db
from ..models.knowledge import KnowledgeBase
from ..models.search_log import SearchLog
from ..utils.logger import get_logger

logger = get_logger(__name__)


def create_knowledge_base(title, content, project_id, category=None, created_by_id=None):
    """ナレッジベースを作成"""
    try:
        knowledge_base = KnowledgeBase(
            title=title,
            content=content,
            project_id=project_id,
            category=category,
            created_by_id=created_by_id
        )
        db.session.add(knowledge_base)
        db.session.commit()
        logger.info(f"ナレッジベース作成: {title} (ID: {knowledge_base.id})")
        return knowledge_base
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"ナレッジベース作成エラー: {str(e)}")
        raise


def get_knowledge_base(kb_id):
    """ナレッジベースを取得"""
    return db.session.get(KnowledgeBase, kb_id)


def get_project_knowledge_bases(project_id):
    """プロジェクトのナレッジベース一覧を取得"""
    return KnowledgeBase.query.filter_by(project_id=project_id).all()


def update_knowledge_base(kb_id, title=None, content=None, category=None):
    """ナレッジベースを更新"""
    try:
        knowledge_base = db.session.get(KnowledgeBase, kb_id)
        if not knowledge_base:
            return None
        
        if title:
            knowledge_base.title = title
        if content is not None:
            knowledge_base.content = content
        if category is not None:
            knowledge_base.category = category
        
        db.session.commit()
        logger.info(f"ナレッジベース更新: {knowledge_base.title} (ID: {kb_id})")
        return knowledge_base
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"ナレッジベース更新エラー: {str(e)}")
        raise


def delete_knowledge_base(kb_id):
    """ナレッジベースを削除"""
    try:
        knowledge_base = KnowledgeBase.query.get(kb_id)
        if not knowledge_base:
            return False
        
        db.session.delete(knowledge_base)
        db.session.commit()
        logger.info(f"ナレッジベース削除: ID {kb_id}")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"ナレッジベース削除エラー: {str(e)}")
        raise


def search_knowledge_base(kb_id, query, user_id=None):
    """ナレッジベース内を検索"""
    try:
        # 検索ロジックをここに実装
        # 実際の検索実装は要件に応じて変更
        results = []
        
        # 検索ログを記録
        if user_id:
            search_log = SearchLog(
                user_id=user_id,
                knowledge_base_id=kb_id,
                query=query
            )
            db.session.add(search_log)
            db.session.commit()
        
        logger.info(f"ナレッジベース検索: KB {kb_id}, クエリ: {query}")
        return results
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"ナレッジベース検索エラー: {str(e)}")
        raise
