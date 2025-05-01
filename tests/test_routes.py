from app.db import db
from app.models.planets import Planet

def test_get_all_planets_returns_empty_list_when_db_is_empty(client):
    # act
    response = client.get("/planets")

    # assert
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_one_planet_returns_seeded_planet(client, one_planet):
    # act
    response = client.get(f"/planets/{one_planet.id}")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert response_body["id"] == one_planet.id
    assert response_body["name"] == one_planet.name
    assert response_body["description"] == one_planet.description
    assert response_body["atmosphere"] == one_planet.atmosphere


def test_create_planet_happy_path(client):
    # arrange
    EXPECTED_PLANET = {
        "name": "Venus",
        "description": "Slightly smaller than Earth",
        "atmosphere": "thick"
    }

    # act
    response = client.post("/planets", json=EXPECTED_PLANET)
    response_body = response.get_json()

    # assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["name"] == EXPECTED_PLANET["name"]
    assert response_body["description"] == EXPECTED_PLANET["description"]
    assert response_body["atmosphere"] == EXPECTED_PLANET["atmosphere"]

    # check that the db was updated
    query = db.select(Planet).where(Planet.id == 1)
    new_planet = db.session.scalar(query)  # compare these values to EXPECTED

    assert new_planet.id == 1
    assert new_planet.name == EXPECTED_PLANET["name"]
    assert new_planet.description == EXPECTED_PLANET["description"]
    assert new_planet.atmosphere == EXPECTED_PLANET["atmosphere"]
