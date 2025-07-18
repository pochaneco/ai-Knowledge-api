# -*- coding: utf-8 -*-
"""
メインビュー（ルートページなど）
"""

from flask import Blueprint, render_template


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """ホームページ"""
    return render_template('index.html')


@main_bp.route('/about')
def about():
    """アバウトページ"""
    return render_template('about.html')


@main_bp.route('/docs')
def docs():
    """ドキュメントページ"""
    return render_template('docs.html')
