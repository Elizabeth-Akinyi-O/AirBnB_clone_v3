#!/usr/bin/python3
"""
Creates a Flask web server to handle api petition-requests
"""

from flask import jsonify, abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def all_cities(state_id):
    """
    Retrieves the list of all city objects
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)
    the_list = []
    for city in state.cities:
        the_list.append(city.to_dict())
    return jsonify(the_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city(city_id):
    """
    Retrieves a City object if id is linked to some City object
    """
    city_obj = storage.get(classes["City"], city_id)
    if city_obj is None:
        abort(404)
    city_obj = city_obj.to_dict()
    return jsonify(city_obj)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_city(city_id):
    """
    Deletes a City object if id is linked to some City object
    """
    city_obj = storage.get(classes["City"], city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_city(state_id):
    """
    Create a new City object
    """
    state_obj = storage.get(classes["State"], state_id)
    if state_obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    if "name" in data_json:
        new_city = classes["City"](state_id=state_id, **data_json)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """
    Update a City object
    """
    city_obj = storage.get(classes["City"], city_id)
    if city_obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(city_obj, key, value)
    storage.save()
    return jsonify(city_obj.to_dict())
