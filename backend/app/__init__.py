from flask import Flask
from flask_migrate import Migrate
from database import db
from .routes import main
from .config import Config

def create_app():
    app = Flask(__name__, static_folder="../../frontend/static", template_folder="../../frontend")
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(main)

    return app
