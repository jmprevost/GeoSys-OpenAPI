from typing import List
import jwt
from swagger_server.utils import utils_gapi
import os

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_geosys_auth(token):

    JWT_SECRET = os.environ.get("GAPI_CRYPTO_SALT")
    JWT_ALGORITHM = os.environ.get("GAPI_JWT_ALGORITHM")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])        
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    #return {'scopes': payload["scope_nom"]}
    return {'scopes': ['read', 'write', 'delete']}

def validate_scope_geosys_auth(required_scopes, token_scopes):
    
    return set(required_scopes).issubset(set(token_scopes))
    


