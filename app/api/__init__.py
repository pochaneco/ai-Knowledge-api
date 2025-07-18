# -*- coding: utf-8 -*-
"""
API初期化モジュール
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

# API v1の登録
from .v1 import api_v1_bp
