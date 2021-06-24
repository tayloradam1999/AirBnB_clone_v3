#!/usr/bin/python3
""" New view for City objects that handles default API actions """

from flask import Flask, Blueprint, jsonify, request, url_for, abort
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
import json


@app_views.route("/cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def show_city_with_id(city_id):
    """ shows specific class with given id """

    data = storage.get(City, city_id)
    if data is None:
        abort(404)
    return jsonify(data.to_dict())


@app_views.route("/states/<state_id>/cities", methods=['GET'], 
                 strict_slashes=False)
def show_all_cities(state_id):
    """ by default, shows all cities of a state """

    states = storage.all(State)
    if "State." + state_id not in states:
        abort(404)
    cities = storage.all(City)
    new_list = []
    for city in cities.values():
        if city.state_id == state_id:
            new_list.append(city.to_dict())
    return jsonify(new_list)


@app_views.route("/states/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_with_id(city_id):
    """ deletes the class associated with given id """

    data = storage.get(City, city_id)
    if data is None:
        abort(404)
    storage.delete(data)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def post_city():
    """ creates something new with parameters """

    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    if "name" not in data:
        abort(400, description="Missing name")

    obj = City(**data)
    storage.new(obj)
    storage.save()
    return obj.to_dict(), 201


@app_views.route("/states/<city_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def put_city(city_id):
    """ updates class with information """

    data = storage.get(City, city_id)

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
