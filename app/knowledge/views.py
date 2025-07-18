# -*- coding: utf-8 -*-
"""
ナレッジベース関連ビュー（Webページ）
"""

from flask import Blueprint, render_template


knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')


@knowledge_bp.route('/')
def index():
    """ナレッジベース一覧ページ"""
    return render_template('knowledge/index.html')


@knowledge_bp.route('/<int:kb_id>')
def detail(kb_id):
    """ナレッジベース詳細ページ"""
    return render_template('knowledge/detail.html', kb_id=kb_id)


@knowledge_bp.route('/create')
def create():
    """ナレッジベース作成ページ"""
    return render_template('knowledge/create.html')


@knowledge_bp.route('/<int:kb_id>/edit')
def edit(kb_id):
    """ナレッジベース編集ページ"""
    return render_template('knowledge/edit.html', kb_id=kb_id)


@knowledge_bp.route('/<int:kb_id>/search')
def search(kb_id):
    """ナレッジベース検索ページ"""
    return render_template('knowledge/search.html', kb_id=kb_id)
