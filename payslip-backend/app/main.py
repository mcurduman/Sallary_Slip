from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, get_jwt
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from app.api.error_handler import register_error_handlers
from app.api.routes_handler import register_routes
from app.utils.email import mail
from app.core.config import get_settings
load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.update(get_settings().model_dump())

register_error_handlers(app)
register_routes(app)

CORS(app)
mail.init_app(app)

JWTManager(app)
@app.context_processor
def inject_user():
   try:
      verify_jwt_in_request()
      claims = get_jwt()
      return {"user": {"email": claims.get("email"), "role": claims.get("role")}}
   except Exception:
      return {"user": None}

if __name__ == "__main__":   
   app.run(debug=True)