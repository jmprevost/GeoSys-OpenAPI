from typing import List
import jwt
from swagger_server.utils import utils_gapi
import os
from flask import g

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_geosys_auth(token):

    JWT_SECRET = os.environ.get("GAPI_CRYPTO_SALT")
    JWT_ALGORITHM = os.environ.get("GAPI_JWT_ALGORITHM")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if set(['admin']).issubset(set(payload["scope_nom"])):
            g.user_admin = True
        else:
            g.user_admin = False
        
        if set(['ALL']).issubset(set(payload["theme_nom"])):
            g.all_themes = True
        else:
            g.all_themes = False

    except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    return {'scopes': payload["scope_nom"]}
    #return {'scopes': ['read', 'write', 'delete']}

def validate_scope_geosys_auth(required_scopes, token_scopes):
    
    if g.get("user_admin") == False:
        return set(required_scopes).issubset(set(token_scopes))
    else:
        return True #l'admin a tous les droits
    


