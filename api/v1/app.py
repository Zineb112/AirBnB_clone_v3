#!/usr/bin/python3
"""
this Flask App integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable: app
app = Flask(__name__)
swagger = Swagger(app)

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Cross-Origin Resource Sharing
cors = CORS(app, resources={r'/*': {'origins': host}})

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session after each request,
    """
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """
       this Global Route that handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """
    This version of HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """
    the main of  Flask App
    """
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port)
