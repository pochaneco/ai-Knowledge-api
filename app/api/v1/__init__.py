# -*- coding: utf-8 -*-
"""
API v1 初期化モジュール
"""

from flask import Blueprint

api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# APIルートのインポート
from . import auth_api, projects_api, knowledge_api
