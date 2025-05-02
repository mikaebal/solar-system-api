from flask import abort, make_response
from ..db import db 

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        invalid = {"message": f"{cls.__name__} id ({model_id}) is invalid."}
        abort(make_response(invalid,400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        not_found = {"message": f"{cls.__name__} with id ({model_id}) was not found."}
        abort(make_response(not_found, 404))

    return model