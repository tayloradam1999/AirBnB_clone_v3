#!/usr/bin/python3
"""Host of our our Flask app"""


from flask import Flask, Blueprint, render_template
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app)


@app.teardown_appcontext
def tearDown(self):
    storage.close()

if __name__ == "__main__":
    app.config.update(
        SERVER_NAME="HBNB_API_HOST:HBNB_API_PORT"
    )
    app.run(host="0.0.0.0", port="5000", threaded=True)
