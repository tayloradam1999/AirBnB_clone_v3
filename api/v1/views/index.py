#!/usr/bin/python3
"""Creates a route that returns a JSON"""

from flask import jsonify
from api.v1.views import app_views
from models.storage import count


@app_views.route("/status", strict_slashes=False)
def return_jsonify():
    """Returns JSON status=OK"""

    return jsonify({"status": "OK"})

@app_views.route("/api/v1/stats", strict_slashes=False)
def endpoint():
    """Retrieves number of each object by type"""
    return jsonify({
        'amenitites': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
})