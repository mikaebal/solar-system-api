from flask import abort, Blueprint, make_response, request
from ..db import db 
from app.models.planets import Planet 

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    atmosphere = request_body["atmosphere"]

    new_planet = Planet(name=name, description=description, atmosphere=atmosphere)
    db.session.add(new_planet)
    db.session.commit()

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
                "title": planet.name,
                "description": planet.description,
                "atmosphere": planet.atmosphere
            }
        )

    return planets_response


# def get_all_planets():
#     planets_response = []
#     for planet in planets:
#         planets_response.append(
#             {
#                 "id": planet.id,
#                 "title": planet.name,
#                 "description": planet.description,
#                 "atmosphere": planet.atmosphere
#             }
#         )
#     return planets_response

# @planets_bp.get("/<id>")
# def get_one_planet(id):
#     planet = validate_planet(id)

#     planet_dict = dict(
#         id = planet.id,
#         title = planet.name,
#         description = planet.description,
#         atmosphere = planet.atmosphere
#     )

#     return planet_dict

# wave 4
# def validate_planet(id):
#     try:
#         id = int(id)
#     except:
#         invalid = {"message": f"Planet id ({id}) is invalid."}
#         abort(make_response(invalid,400))

#     for planet in planets:
#         if planet.id == id:
#             return planet

#     not_found = {"message": f"Planet with id ({id}) was not not found."}
#     abort(make_response(not_found, 404))