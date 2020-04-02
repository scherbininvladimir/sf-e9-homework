import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from config import Config

from werkzeug.debug import DebuggedApplication

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

from app import routes, models, forms

