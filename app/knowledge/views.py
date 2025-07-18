# -*- coding: utf-8 -*-
"""
ナレッジベース関連ビュー（Webページ）
"""

from flask import Blueprint
from app.inertia_config import render


knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')


@knowledge_bp.route('/')
def index():
    """ナレッジベース一覧ページ"""
    return render('knowledge/Index')


@knowledge_bp.route('/<int:kb_id>')
def detail(kb_id):
    """ナレッジベース詳細ページ"""
    return render('knowledge/Detail', {'kb_id': kb_id})


@knowledge_bp.route('/create')
def create():
    """ナレッジベース作成ページ"""
    return render('knowledge/Create')


@knowledge_bp.route('/<int:kb_id>/edit')
def edit(kb_id):
    """ナレッジベース編集ページ"""
    return render('knowledge/Edit', {'kb_id': kb_id})


@knowledge_bp.route('/<int:kb_id>/search')
def search(kb_id):
    """ナレッジベース検索ページ"""
    return render('knowledge/Search', {'kb_id': kb_id})
