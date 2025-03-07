#!/usr/bin/python3
""" New view for Place objects that handles default API actions """

from flask import Flask, Blueprint, jsonify, request, url_for, abort
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.city import City
import json


@app_views.route("/places/<string:place_id>", methods=['GET'],
                 strict_slashes=False)
def show_place_with_id(place_id):
    """ shows specific class with given id """

    data = storage.get(Place, place_id)
    if data is None:
        abort(404)
    return jsonify(data.to_dict())


@app_views.route("/cities/<string:city_id>/places", methods=['GET'],
                 strict_slashes=False)
def show_all_places(city_id):
    """ by default, shows all places """

    cities = storage.all(City)
    if "City." + city_id not in cities:
        abort(404)
    places = storage.all(Place)
    new_list = []
    for place in places.values():
        if place.city_id == city_id:
            new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route("/places/<string:place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_with_id(place_id):
    """ deletes the class associated with given id """

    data = storage.get(Place, place_id)
    if data is None:
        abort(404)
    storage.delete(data)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<string:city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    """ creates something new with parameters """

    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    if "name" not in data:
        abort(400, description="Missing name")

    data["city_id"] = city_id

    cities = storage.all(City)
    if "City." + city_id not in cities:
        abort(404)

    if storage.get(User, data["user_id"]) is None:
        abort(404)

    obj = Place(**data)
    storage.new(obj)
    storage.save()
    return obj.to_dict(), 201


@app_views.route("/places/<place_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def put_places(place_id):
    """ updates class with information """

    data = storage.get(Place, place_id)

    if not data:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    my_req = request.get_json()

    for k, v in my_req.items():
        if k != "id" and k != "created_at" and k != "updated_at" and\
           k != "user_id" and k != "city_id":
            setattr(data, k, v)

    storage.save()
    return data.to_dict(), 200
