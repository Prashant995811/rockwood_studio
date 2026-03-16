from pathlib import Path

from flask import Flask, render_template

from config import Config

from .extensions import db
from .routes.admin import admin_bp
from .routes.public import public_bp
from .utils.helpers import get_settings
from .utils.schema import ensure_schema_updates
from .utils.seed import ensure_default_admin, ensure_default_settings


def create_app():
    project_root = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_site_settings():
        return {"site_settings": get_settings()}

    register_error_handlers(app)

    with app.app_context():
        db.create_all()
        ensure_schema_updates()
        ensure_default_admin()
        ensure_default_settings()

    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html", title="Page Not Found"), 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template("errors/500.html", title="Server Error"), 500
