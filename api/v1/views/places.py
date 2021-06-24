#!/usr/bin/python3
""" New view for Place objects that handles default API actions """

from flask import Flask, Blueprint, jsonify, request, url_for, abort
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.places import Place
from models.cities import City
import json


@app_views.route("/places/<string:place_id>", methods=['GET'],
                 strict_slashes=False)
def show_with_id(place_id):
    """ shows specific class with given id """

    data = storage.get(Place, place_id)
    if data is None:
        abort(404)
    return jsonify(data.to_dict())


@app_views.route("/places", methods=['GET'], strict_slashes=False)
def show_all():
    """ by default, shows all places """

    places = storage.all(Place).values()
    new_list = []
    for place in places:
        new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route("/places/<string:place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_with_id(place_id):
    """ deletes the class associated with given id """

    data = storage.get(Place, place_id)
    if data is None:
        abort(404)
    storage.delete(data)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<string:city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post(city_id):
    """ creates something new with parameters """

    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    data["city_id"] = city_id

    cities = storage.all(City)
    if "City." + city_id not in cities:
        abort(404)

    if "name" not in data:
        abort(400, description="Missing name")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    obj = Place(**data)
    storage.new(obj)
    storage.save()
    return obj.to_dict(), 201


@app_views.route("/places/<place_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def put(place_id):
    """ updates class with information """

    data = storage.get(Place, place_id)

    if not data:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    my_req = request.get_json()

    for k, v in my_req.items():
        if k != "id" and k != "created_at" and k != "updated_at"
        and k != "user_id" and k != "city_id":
            setattr(data, k, v)

    storage.save()
    return data.to_dict(), 200
