from flask import Flask

from routes.main_routes import main
from routes.auth_routes import auth

from database.db import create_tables

app = Flask(__name__)

app.secret_key = "focusflow_secret_key"

app.register_blueprint(main)
app.register_blueprint(auth)

create_tables()

if __name__ == "__main__":
    app.run(debug=True)
