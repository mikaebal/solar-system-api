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




# --- WAVE 4 -------
# https://github.com/AdaGold/solar-system-api/blob/main/project-directions/wave_04.md



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


def validate_planet(id):
    try:
        id = int(id)
    except:
        invalid = {"message": f"Planet id ({id}) is invalid."}
        abort(make_response(invalid,400))

    #Write SQL to SELECT * FROM planets; --> in SQLAlchemy syntax
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query) # planets is a list

    for planet in planets:
        if planet.id == id:
            return planet

    not_found = {"message": f"Planet with id ({id}) was not not found."}
    abort(make_response(not_found, 404))


# PATCH(partial) request with valid planet data to update one existing planet and get a 201 response
@planets_bp.route('/<int:item_id>', methods=['PATCH'])
def update_one_planet(id):
    planet = validate_planet(id)

    data = get_all_planets()

    updated_data = request.get_json() #parses incoming request data that is in JSON format and converts to a Python dictionary
    
    # How do we access our Planets dictionary (SQL table) 
    
    # How do we update the description key to a new value




# 404 for non existing planet and 400 for invalid planet_id

# DELETE request for an existing planet and get a 200 ok response
# 404 for non existing planet and 400 for invalid planet_id



@app.route('/data', methods=['GET', 'PATCH'])

def handle_data():
    if request.method == 'GET':
        return jsonify(data)
    elif request.method == 'PATCH':
        data.update(request.get_json())
        return jsonify(data)
