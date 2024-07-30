from flask import Flask, request
from flask import current_app as app

from controllers.actor import (
    get_all_actors, get_actor_by_id, add_actor, update_actor, delete_actor,
    actor_add_relation, actor_clear_relations
)
from controllers.movie import (
    get_all_movies, get_movie_by_id, add_movie, update_movie, delete_movie,
    movie_add_relation, movie_clear_relations
)


@app.route('/api/actors', methods=['GET'])
def actors():
    """
    Get all actors in db
    """
    return get_all_actors()


@app.route('/api/movies', methods=['GET'])
def movies():
    """
    Get all movies in db
    """
    return get_all_movies()


@app.route('/api/actor', methods=['GET', 'POST', 'PUT', 'DELETE'])
def actor():
    """
    Manipulate with actors records
    GET: get actor by id
    POST: add new actor
    PUT: update actor
    DELETE: remove actor
    """
    if request.method == 'GET':
        return get_actor_by_id()
    elif request.method == 'POST':
        return add_actor()
    elif request.method == 'PUT':
        return update_actor()
    elif request.method == 'DELETE':
        return delete_actor()


@app.route('/api/movie', methods=['GET', 'POST', 'PUT', 'DELETE'])
def movie():
    """
    Manipulate with movies records
    GET: get movie by id
    POST: add new movie
    PUT: update movie
    DELETE: remove movie
    """
    if request.method == 'GET':
        return get_movie_by_id()
    elif request.method == 'POST':
        return add_movie()
    elif request.method == 'PUT':
        return update_movie()
    elif request.method == 'DELETE':
        return delete_movie()


@app.route('/api/actor-relations', methods=['PUT', 'DELETE'])
def actor_relation():
    """
    Manipulate with actor's relations
    PUT: add relations
    DELETE: clear relations
    """
    if request.method == 'PUT':
        return actor_add_relation()
    elif request.method == 'DELETE':
        return actor_clear_relations()


@app.route('/api/movie-relations', methods=['PUT', 'DELETE'])
def movie_relation():
    """
    Manipulate with movie's relations
    PUT: add relations
    DELETE: clear relations
    """
    if request.method == 'PUT':
        return movie_add_relation()
    elif request.method == 'DELETE':
        return movie_clear_relations()
