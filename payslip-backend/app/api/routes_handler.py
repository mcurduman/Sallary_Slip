from app.api.routers.auth import auth

def register_routes(app):
    app.register_blueprint(auth, url_prefix="/api/auth")