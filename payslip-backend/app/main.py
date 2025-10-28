from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, get_jwt
from flask_jwt_extended.view_decorators import verify_jwt_in_request
import os

mail = Mail()

app = Flask(__name__)
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL")
app.config["MAIL_ASCII_ATTACHMENTS"] = os.getenv("MAIL_ASCII_ATTACHMENTS")
CORS(app)

mail.init_app(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = os.getenv("JWT_TOKEN_LOCATION").split(",")
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_COOKIE_SECURE"] = os.getenv("JWT_COOKIE_SECURE")
app.config["JWT_COOKIE_SAMESITE"] = os.getenv("JWT_COOKIE_SAMESITE")
app.config["JWT_ACCESS_COOKIE_PATH"] = os.getenv("JWT_ACCESS_COOKIE_PATH")
app.config["JWT_REFRESH_COOKIE_PATH"] = os.getenv("JWT_REFRESH_COOKIE_PATH")

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