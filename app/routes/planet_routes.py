from flask import Blueprint, request, Response
from .route_utilities import validate_model
from ..db import db 
from app.models.planets import Planet 

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    new_planet = Planet.from_dict(request_body) #make instance of planet class
    
    db.session.add(new_planet) # stage instance to add to the db
    db.session.commit() # adds instance to the db

    return new_planet.to_dict(), 201

@planets_bp.get("")
def get_all_planets():
    query = db.select(Planet)

    # query = db.select(Planet).order_by(Planet.id)
    # planets = db.session.scalars(query)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Planet.name == name_param)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    atmosphere_param = request.args.get("atmosphere")
    if atmosphere_param:
        query = query.where(Planet.atmosphere.ilike(f"%{atmosphere_param}%"))

    query = query.order_by(Planet.name.desc())
    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(planet.to_dict())

    return planets_response


@planets_bp.get("/<id>")
def get_one_planet(id):
    planet = validate_model(Planet, id)

    return planet.to_dict()

@planets_bp.put("/<id>")
def update_planet(id):
    planet = validate_model(Planet, id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.atmosphere = request_body["atmosphere"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<id>")
def delete_planet(id):
    planet = validate_model(Planet, id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
