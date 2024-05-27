#!/usr/bin/python3
"""
Creates a Flask web server to handle api petition-requests
"""
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, origins="0.0.0.0")
api_host = getenv('HBNB_API_HOST', "0.0.0.0")
api_port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def commit_data(error):
    """
    Commit changes in database
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    returns a JSON-formatted 404 status code response
    Args:
        error: error message received
    """
    error_msg = {"error": "Not found"}
    return jsonify(error_msg), 404


if __name__ == "__main__":
    app.run(host=api_host, port=int(api_port), threaded=True)
