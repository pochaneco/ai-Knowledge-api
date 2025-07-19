# -*- coding: utf-8 -*-
"""
メインビュー（ルートページなど）
"""

from flask import Blueprint
from app.inertia_config import render


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """ホームページ"""
    return render('Home/Home')


@main_bp.route('/about')
def about():
    """アバウトページ"""
    return render('About')


@main_bp.route('/docs')
def docs():
    """ドキュメントページ"""
    return render('Docs')
