# -*- coding: utf-8 -*-
"""
ロガー設定
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    """アプリケーションのロガーを設定"""
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # ファイルハンドラーの設定
        file_handler = RotatingFileHandler(
            'logs/app.log', 
            maxBytes=10240000, 
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('アプリケーション起動')


def get_logger(name):
    """指定された名前のロガーを取得"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # コンソールハンドラーの設定
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)
    
    return logger
