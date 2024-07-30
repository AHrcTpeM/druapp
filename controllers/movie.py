from flask import jsonify, make_response

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mv = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mv)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
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

        obj = Movie.query.filter_by(id=row_id).first()
        if obj:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
            return make_response(jsonify(movie), 200)
        else:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    required_fields = {'name', 'year', 'genre'}
    allowed_fields = required_fields

    if not required_fields.issubset(data.keys()):
        err = 'Missing required fields'
        return make_response(jsonify(error=err), 400)

    # Check for extra fields
    if not set(data.keys()).issubset(allowed_fields):
        err = 'Contains extra fields'
        return make_response(jsonify(error=err), 400)

    if 'year' in data:
        try:
            data['year'] = int(data['year'])
        except ValueError:
            err = 'Year must be integer'
            return make_response(jsonify(error=err), 400)

    new_record = Movie.create(**data)
    new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie), 200)


def update_movie():
    """
    Update movie record by id
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

    obj = Movie.query.filter_by(id=row_id).first()
    if not obj:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    ACTOR_FIELDS = {'name', 'year', 'genre'}
    allowed_fields = set(ACTOR_FIELDS) | {'id'}
    # Check for non-existing fields
    if not set(data.keys()).issubset(allowed_fields):
        err = 'Contains non-existing fields'
        return make_response(jsonify(error=err), 400)

    if 'year' in data:
        try:
            data['year'] = int(data['year'])
        except ValueError:
            err = 'Year must be integer'
            return make_response(jsonify(error=err), 400)

    upd_record = Movie.update(row_id, **data)
    upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(upd_movie), 200)


def delete_movie():
    """
    Delete movie by id
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

    obj = Movie.query.filter_by(id=row_id).first()
    if not obj:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    Movie.delete(row_id)
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    if 'id' not in data.keys() or 'relation_id' not in data.keys():
        err = 'id and relation_id must be specified'
        return make_response(jsonify(error=err), 400)

    try:
        movie_id = int(data['id'])
        actor_id = int(data['relation_id'])
    except ValueError:
        err = 'Actor id and movie id must be integer'
        return make_response(jsonify(error=err), 400)

    actor = Actor.query.filter_by(id=actor_id).first()
    movie = Movie.query.filter_by(id=movie_id).first()
    if not actor or not movie:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    movie = Movie.add_relation(movie_id, actor)
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)


def movie_clear_relations():
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

    movie = Movie.query.filter_by(id=row_id).first()
    if not movie:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    movie = Movie.clear_relations(row_id)
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)
