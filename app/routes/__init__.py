from .recipe import recipe_bp

def register_routes(app):
    """
    註冊所有的 Flask Blueprints 到 app 實例
    """
    app.register_blueprint(recipe_bp)
