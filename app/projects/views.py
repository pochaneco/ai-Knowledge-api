# -*- coding: utf-8 -*-
"""
プロジェクトビュー（Webページ）
"""

from flask import Blueprint
from app.inertia_config import render


project_bp = Blueprint('project', __name__, url_prefix='/projects')


@project_bp.route('/')
def index():
    """プロジェクト一覧ページ"""
    return render('projects/Index')


@project_bp.route('/<int:project_id>')
def detail(project_id):
    """プロジェクト詳細ページ"""
    return render('projects/Detail', {'project_id': project_id})


@project_bp.route('/create')
def create():
    """プロジェクト作成ページ"""
    return render('projects/Create')


@project_bp.route('/<int:project_id>/edit')
def edit(project_id):
    """プロジェクト編集ページ"""
    return render('projects/Edit', {'project_id': project_id})


@project_bp.route('/<int:project_id>/members')
def members(project_id):
    """プロジェクトメンバー管理ページ"""
    return render('projects/Members', {'project_id': project_id})
