from flask import Blueprint, request, Response
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db 
from app.models.planets import Planet 
from app.models.moon import Moon

bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@bp.post("")
def create_planet():
    request_body = request.get_json()

    return create_model(Planet, request_body)

    # new_planet = Planet.from_dict(request_body) #make instance of planet class
    
    # db.session.add(new_planet) # stage instance to add to the db
    # db.session.commit() # adds instance to the db

    # return new_planet.to_dict(), 201



@bp.get("")
def get_all_planets():
    return get_models_with_filters(Planet, request.args)

    # query = db.select(Planet)

    # # query = db.select(Planet).order_by(Planet.id)
    # # planets = db.session.scalars(query)

    # name_param = request.args.get("name")
    # if name_param:
    #     query = query.where(Planet.name == name_param)

    # description_param = request.args.get("description")
    # if description_param:
    #     query = query.where(Planet.description.ilike(f"%{description_param}%"))

    # atmosphere_param = request.args.get("atmosphere")
    # if atmosphere_param:
    #     query = query.where(Planet.atmosphere.ilike(f"%{atmosphere_param}%"))

    # query = query.order_by(Planet.name.desc())
    # planets = db.session.scalars(query)

    # planets_response = []
    # for planet in planets:
    #     planets_response.append(planet.to_dict())

    # return planets_response


@bp.get("/<id>")
def get_one_planet(id):
    planet = validate_model(Planet, id)

    return planet.to_dict()

@bp.put("/<id>")
def update_planet(id):
    planet = validate_model(Planet, id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.atmosphere = request_body["atmosphere"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("/<id>")
def delete_planet(id):
    planet = validate_model(Planet, id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# nested route
# adds a new moon to a specific planet
@bp.post("/planets/<planet_id>/moons")
def create_moon_for_planet(id):
    planet = validate_model(Planet, id)
    request_body = request.get_json()

    moon_data = {
        "size": request_body["size"],
        "description": request_body["description"],
        "orbital_period": request_body["orbital_period"],
        "planet": planet
    }

    return create_model(Moon, moon_data)

# nested route
# gets all moons associated with a specific planet
@bp.get("/planets/<planet_id>/moons")
def get_moons_for_planet(id):
    planet = validate_model(Planet, id)
    moons = [moon.to_dict() for moon in planet.moons]
    return moons, 200
