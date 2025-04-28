from flask import abort, Blueprint, make_response, request, Response
from ..db import db 
from app.models.planets import Planet 

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    atmosphere = request_body["atmosphere"]

    new_planet = Planet(name=name, description=description, atmosphere=atmosphere) #make instance of planet class
    db.session.add(new_planet) # stage instance to add to the db
    db.session.commit() # adds instance to the db

    planets_response = {
                "id": new_planet.id,
                "name": new_planet.name,
                "description": new_planet.description,
                "atmosphere": new_planet.atmosphere
    }

    return planets_response, 201

@planets_bp.get("")
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)

    # planet = validate_planet(id)
    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "atmosphere": planet.atmosphere
            }
        )

    return planets_response


@planets_bp.get("/<id>")
def get_one_planet(id):
    planet = validate_planet(id)

    planet_dict = dict(
        id = planet.id,
        name = planet.name,
        description = planet.description,
        atmosphere = planet.atmosphere
    )

    return planet_dict

@planets_bp.put("/<id>")
def update_planet(id):
    planet = validate_planet(id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.atmosphere = request_body["atmosphere"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<id>")
def delete_planet(id):
    planet = validate_planet(id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def validate_planet(id):
    try:
        id = int(id)
    except ValueError:
        invalid = {"message": f"Planet id ({id}) is invalid."}
        abort(make_response(invalid,400))

    query = db.select(Planet).where(Planet.id == id)
    planet = db.session.scalar(query)

    if not planet:
        not_found = {"message": f"Planet with id ({id}) was not not found."}
        abort(make_response(not_found, 404))

    return planet
