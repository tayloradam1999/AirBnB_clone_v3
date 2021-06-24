#!/usr/bin/python3
""" New view for Amenity objects that handles default API actions """

from flask import Flask, Blueprint, jsonify, request, url_for, abort
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
import json


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def show_amenity_with_id(amenity_id):
    """ shows specific class with given id """

    data = storage.get(Amenity, amenity_id)
    if data is None:
        abort(404)
    return jsonify(data.to_dict())


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def show_all_amenities():
    """ by default, shows all amenities """

    amenities = storage.all(Amenity).values()
    new_list = []
    for amenity in amenities:
        new_list.append(amenity.to_dict())
    return jsonify(new_list)


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_with_id(amenity_id):
    """ deletes the class associated with given id """

    data = storage.get(Amenity, amenity_id)
    if data is None:
        abort(404)
    storage.delete(data)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ creates something new with parameters """

    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    if "name" not in data:
        abort(400, description="Missing name")

    obj = Amenity(**data)
    storage.new(obj)
    storage.save()
    return obj.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ updates class with information """

    data = storage.get(Amenity, amenity_id)

    if not data:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    my_req = request.get_json()

    for k, v in my_req.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(data, k, v)

    storage.save()
    return data.to_dict(), 200
