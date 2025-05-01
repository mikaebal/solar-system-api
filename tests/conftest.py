import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.planets import Planet

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_planet(app):
    planet = Planet(
        name="Mercury",
        description="Highly eccentric orbit",
        atmosphere="thin"
    )
    db.session.add(planet)
    db.session.commit()
    return planet

