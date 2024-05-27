#!/usr/bin/python3
"""
Creates a Flask web server to handle api petition-requests
"""
from flask import jsonify, abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    objects = storage.all("Amenity")
    obj_list = []
    for obj in objects.values():
        obj_list.append(obj.to_dict())
    return jsonify(obj_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def amenity(amenity_id):
    """
    Retrieves an Amenity object if id is linked to some Amenity object
    """
    amenity_obj = storage.get(classes["Amenity"], amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_obj = amenity_obj.to_dict()
    return jsonify(amenity_obj)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_amenity(amenity_id):
    """
    Deletes an Amenity object if id is linked to some Amenity object
    """
    amenity_obj = storage.get(classes["Amenity"], amenity_id)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """
    Create a new Amenity object
    """
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    if "name" in data_json:
        new_amenity = classes["Amenity"](**data_json)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route('amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def put_amenity(amenity_id):
    """
    Update an Amenity object
    """
    obj = storage.get(classes["Amenity"], amenity_id)
    if obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
