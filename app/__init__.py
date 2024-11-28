from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import pandas as pd
import os
from pathlib import Path

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login' 
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    # features for prediction
    DEPLOY_FEATURE_FILENAME = "deploy_feature_names_v2.csv"
    APP_DATA_PATH = Path(os.getcwd()) / "app" / "static" / "data"
    DEPLOY_FEATURE_PATH = APP_DATA_PATH / DEPLOY_FEATURE_FILENAME
    app.features = pd.read_csv(DEPLOY_FEATURE_PATH)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app 

from app import models 