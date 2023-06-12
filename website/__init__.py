from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "bmi-calculating-device"

    from .api.firebase import DatabaseService

    db = DatabaseService()
    db.setup_database()

    from . import views

    app.register_blueprint(views.bp, url_prefix="/")

    return app
