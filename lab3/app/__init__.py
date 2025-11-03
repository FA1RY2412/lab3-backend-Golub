
from flask import Flask
from flask_smorest import Api
from .db import db, migrate
import os

def create_app(test_config=None):
    app = Flask(__name__)

    # Basic API/Swagger config for flask-smorest
    app.config.update({
        "API_TITLE": "Expenses API (Lab 3)",
        "API_VERSION": "v1",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_URL_PREFIX": "/",
        "OPENAPI_SWAGGER_UI_PATH": "/docs",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    })

    # Load config from file if present, then from env
    app.config.from_pyfile('config.py', silent=True)

    # If env var is set, override file config
    db_uri = os.environ.get("DATABASE_URL")
    if db_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///local.db")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    # Register blueprints
    from .resources.category import blp as CategoryBlp
    from .resources.expense import blp as ExpenseBlp

    api.register_blueprint(CategoryBlp, url_prefix="/api/categories")
    api.register_blueprint(ExpenseBlp, url_prefix="/api/expenses")

    # Simple health endpoint
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
