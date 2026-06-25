from flask import Flask
from .extensions import db, migrate, login_manager
from .models import User  # ensure models are imported for migrations

import os

def create_app():
    """
    Application factory: creates and configures the Flask app instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Config loading: default config + .env via environment variables
    app.config.from_object("config.Config")

    # Ensure instance/ exists (for SQLite, uploads, etc.)
    os.makedirs(app.instance_path, exist_ok=True)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .teams.routes import teams_bp
    from .players.routes import players_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(teams_bp)
    app.register_blueprint(players_bp)
    return app
