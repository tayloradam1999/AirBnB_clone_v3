#!/usr/bin/python3
""" New view for Stat objects that handles default API actions """

from flask import Flask, Blueprint, jsonify, request, url_for
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", methods=['GET'], strict_slashes=False)
def show_all():
    """ by default, shows all states """
    
    states = storage.all(State).values()
    
    if request.method == 'GET':
        new_list = []
        for state in states:
            new_list.append(state.to_dict())
        return jsonify(new_list)
