import os
from flask import Flask

def create_app(test_config=None):
    # 建立並設定 app
    app = Flask(__name__, instance_relative_config=True)
    
    # 載入預設設定
    app.config.from_mapping(
        SECRET_KEY='dev_default_secret',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # 在非測試環境時，載入全域的 config.py
        app.config.from_object('config.Config')
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 目錄存在 (SQLite 資料庫會放在這裡)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊路由 Blueprints
    from .routes.recipe import recipe_bp
    app.register_blueprint(recipe_bp)

    return app
