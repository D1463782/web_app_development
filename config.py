import os

class Config:
    """基礎設定"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_default_secret')
    # 預設會被 app/__init__.py 中的設定覆寫或繼承
