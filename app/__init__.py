from flask import Flask
from .db import db, migrate
from .routes.planet_routes import planets_bp
from .models import planets


# def create_app(test_config=None):
#     app = Flask(__name__)

#     app.register_blueprint(planets_bp)

#     return app

# ---------------------------------------------------------------
# SQLALCHEMY CONNECTION SETUP

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/solar_system_developement'

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(planets_bp)

    return app