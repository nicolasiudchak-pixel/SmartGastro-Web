from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///smartgastro.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WEATHER_API_KEY"] = os.getenv("WEATHER_API_KEY", "")
    app.config["WEATHER_CITY"] = os.getenv("WEATHER_CITY", "Buenos Aires")

    db.init_app(app)
    bcrypt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.productos import productos_bp
    from .routes.clientes import clientes_bp
    from .routes.ventas import ventas_bp
    from .routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(ventas_bp, url_prefix="/ventas")
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        from . import models
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    from .models import Usuario
    if not Usuario.query.filter_by(email="admin@smartgastro.com").first():
        admin = Usuario(
            nombre="Admin",
            email="admin@smartgastro.com",
            password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            rol="admin",
        )
        try:
            db.session.add(admin)
            db.session.commit()
        except Exception:
            db.session.rollback()
