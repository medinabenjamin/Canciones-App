from flask import Flask

from app.extensions import bcrypt, db, login_manager, migrate
from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.songs import songs_bp
from config import get_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor inicia sesión para continuar."

    from app import models  # noqa: F401

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(songs_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return models.Usuario.query.get(int(user_id))

    from app.services.bootstrap import ensure_roles_and_admin

    with app.app_context():
        ensure_roles_and_admin()

    return app
