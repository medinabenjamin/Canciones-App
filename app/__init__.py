from flask import Flask

from app.extensions import db, migrate
from app.routes.main import main_bp
from config import get_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401

    app.register_blueprint(main_bp)

    return app
