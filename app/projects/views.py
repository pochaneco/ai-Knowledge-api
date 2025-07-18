# -*- coding: utf-8 -*-
"""
プロジェクトルーティング設定
"""

from flask import Blueprint, render_template


project_bp = Blueprint('project', __name__, url_prefix='/projects')


@project_bp.route('/')
def index():
    """プロジェクト一覧ページ"""
    return render_template('projects/index.html')


@project_bp.route('/<int:project_id>')
def detail(project_id):
    """プロジェクト詳細ページ"""
    return render_template('projects/detail.html', project_id=project_id)


@project_bp.route('/create')
def create():
    """プロジェクト作成ページ"""
    return render_template('projects/create.html')


@project_bp.route('/<int:project_id>/edit')
def edit(project_id):
    """プロジェクト編集ページ"""
    return render_template('projects/edit.html', project_id=project_id)


@project_bp.route('/<int:project_id>/members')
def members(project_id):
    """プロジェクトメンバー管理ページ"""
    return render_template('projects/members.html', project_id=project_id)
