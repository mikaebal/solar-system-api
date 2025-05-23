from flask import Flask
from .db import db, migrate
from .routes.planet_routes import bp as planets_bp
from .models import planets, moon
import os
from dotenv import load_dotenv
from .routes.moon_routes import bp as moon_bp

load_dotenv()

# def create_app(test_config=None):
#     app = Flask(__name__)

#     app.register_blueprint(planets_bp)

#     return app

# ---------------------------------------------------------------
# SQLALCHEMY CONNECTION SETUP

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # hardcoded
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+st:5432/solar_system_developement'

    # sets value from development database in .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(planets_bp)
    app.register_blueprint(moon_bp)

    return app