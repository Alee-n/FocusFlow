from flask import Flask
from routes.api_routes import api
from routes.main_routes import main
from routes.auth_routes import auth
from dotenv import load_dotenv
from database.db import create_tables
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

load_dotenv()

app.secret_key = "focusflow_secret_key"

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(api)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
