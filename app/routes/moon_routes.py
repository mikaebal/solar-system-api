from flask import Blueprint, request, Response
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db 
from app.models.planets import Planet 
from app.models.moon import Moon

bp = Blueprint("moons_bp", __name__, url_prefix="/moons")

@bp.post("")
def create_moon():
    request_body = request.get_json()
    return create_model(Moon, request_body)

# get all moons with optional filters
@bp.get("")
def get_all_moons():
    return get_models_with_filters(Moon, request.args)

# get a specific moon
@bp.get("/<id>")
def get_moon_by_id(id):
    moon = validate_model(Moon, id)
    return moon.to_dict(), 200
