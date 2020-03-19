#!/usr/bin/env python3

from swagger_server import encoder

from swagger_server import config

from swagger_server.config import app
from swagger_server.config import db
from swagger_server.config import db_view_session

from flask import Response, request
from flask import jsonify


connex_app = config.connex_app
connex_app.add_api('swagger.yaml', arguments={'title': 'geosys-api'}, pythonic_params=True)
connex_app.app.json_encoder = encoder.JSONEncoder

@app.errorhandler(Exception)
def your_exception_handler(exception):    
    
    db.session.rollback()
    
    if isinstance(exception.args[0], Response):
        return exception.args[0]
    else:
        return jsonify(message=str(exception)), 500

@app.teardown_request
def teardown_request_func(error=None):
    print("Teardown!!!")
    db.session.commit()
    db.session.remove()
    db_view_session.remove()

#if __name__ == '__main__':
#    connex_app.run(port=8080)
