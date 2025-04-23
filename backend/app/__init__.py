"""
Init for app.
"""
from flask import Flask
from flask_migrate import Migrate
from database.models import db
from .routes import main
from .tasks import UpdateActiveAlertsNews, UpdateActiveShellings, UpdateAnalytics

def create_app():
    """
    Creates and configures the Flask application.

    This function initializes the Flask application, sets up the database connection,
    registers Blueprints, and initializes background task managers.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__, static_folder="../../frontend/static", template_folder="../../frontend")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///active_alerts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(main)

    app.updater_alarms_news = UpdateActiveAlertsNews(app)
    app.updater_shellings = UpdateActiveShellings(app)
    app.updater_analytics = UpdateAnalytics(app)

    return app
