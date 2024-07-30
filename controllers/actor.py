from flask import jsonify, make_response
from datetime import datetime as dt
from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS, DATE_FORMAT  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except ValueError:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        if obj:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
            return make_response(jsonify(actor), 200)
        else:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    required_fields = {'name', 'gender', 'date_of_birth'}
    allowed_fields = required_fields
    print('data', data)

    if not required_fields.issubset(data.keys()):
        err = 'Missing required fields'
        return make_response(jsonify(error=err), 400)

    # Check for extra fields
    if not set(data.keys()).issubset(allowed_fields):
        err = 'Contains extra fields'
        return make_response(jsonify(error=err), 400)

    if 'date_of_birth' in data:
        try:
            data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
        except ValueError:
            err = 'Date of birth must be in format ' + DATE_FORMAT
            return make_response(jsonify(error=err), 400)

    new_record = Actor.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        row_id = int(data['id'])
    except ValueError:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    obj = Actor.query.filter_by(id=row_id).first()
    if not obj:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    ACTOR_FIELDS = {'name', 'gender', 'date_of_birth'}
    allowed_fields = set(ACTOR_FIELDS) | {'id'}
    # Check for non-existing fields
    if not set(data.keys()).issubset(allowed_fields):
        err = 'Contains non-existing fields'
        return make_response(jsonify(error=err), 400)

    if 'date_of_birth' in data:
        try:
            data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
        except ValueError:
            err = 'Date of birth must be in format ' + DATE_FORMAT
            return make_response(jsonify(error=err), 400)

    upd_record = Actor.update(row_id, **data)
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        row_id = int(data['id'])
    except ValueError:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    obj = Actor.query.filter_by(id=row_id).first()
    if not obj:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    Actor.delete(row_id)
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    print('actor_add_relation', data)
    if 'id' not in data.keys() or 'relation_id' not in data.keys():
        err = 'id and relation_id must be specified'
        return make_response(jsonify(error=err), 400)

    try:
        actor_id = int(data['id'])
        movie_id = int(data['relation_id'])
    except ValueError:
        err = 'Actor id and movie id must be integer'
        return make_response(jsonify(error=err), 400)

    actor = Actor.query.filter_by(id=actor_id).first()
    movie = Movie.query.filter_by(id=movie_id).first()
    if not actor or not movie:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    actor = Actor.add_relation(actor_id, movie)
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        row_id = int(data['id'])
    except ValueError:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    actor = Actor.query.filter_by(id=row_id).first()
    if not actor:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    actor = Actor.clear_relations(row_id)
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)
