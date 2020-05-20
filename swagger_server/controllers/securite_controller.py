# coding: utf-8
import connexion
import six

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.return_value_basic_error_message import ReturnValueBasicErrorMessage  # noqa: E501
from swagger_server.models.securite_reponse_login import SecuriteReponseLogin  # noqa: E501
from swagger_server.models.usager import Usager  # noqa: E501
from swagger_server import util

# Ajoute manuellement. Ne provient pas du generateur de code
from swagger_server.utils import utils_security
from swagger_server.utils import utils_gapi
from swagger_server.utils import erreurs
from swagger_server.config import db
from swagger_server.db_models.suivi_prod_db_schema import *
from swagger_server.db_models.api_db_schema import *

from flask import request
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken

import jwt
from datetime import datetime, timedelta

def delete_securite_usager_nom(nom):  # noqa: E501
    """delete_securite_usager_nom

     # noqa: E501

    :param nom: 
    :type nom: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def get_securite_login(usager=None, mot_de_passe=None, duree_token=None):  # noqa: E501
    """get_securite_login

    Valide un usager et retourne un jeton (token). # noqa: E501

    :param usager: 
    :type usager: str
    :param mot_de_passe: 
    :type mot_de_passe: str
    :param duree_token: Durée de vie du token en secondes.
    :type duree_token: int

    :rtype: SecuriteReponseLogin
    """

    duree_token = 8000
    # Lecture des parametres de l'appel
    usager = request.headers.get("usager")
    mot_de_passe = request.headers.get("mot_de_passe")
    duree_token = request.headers.get("duree_token")
    
    # Requête dans la table d'usager
    try:
        res = UsagerGeosys.query.filter(UsagerGeosys.nom_usager == usager).one()
        MASerializer = UsagerGeosysSchema()
        user_data = MASerializer.dump(res)
    
    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    # Validation du mot de passe obtenu de la BD    
    encrypt_pwd = str(user_data['mot_de_passe'])
    if not utils_security.password_checker(mot_de_passe, encrypt_pwd):        
        raise Exception(utils_gapi.message_erreur(erreurs.GAPIInvalidPassword(), 400))        

    # Construction du Token
    JWT_EXP_DELTA_SECONDS = int(duree_token)
    JWT_SECRET = os.environ.get("GAPI_CRYPTO_SALT")
    JWT_ALGORITHM = os.environ.get("GAPI_JWT_ALGORITHM")
    
    #Aller chercher dans la BD les noms équivalent aux codes
    themes_nom = utils_gapi.convert_code_to_name(user_data["themes"])
    scopes_nom = utils_gapi.convert_code_to_name(user_data["scopes"])
    equipes_nom = utils_gapi.convert_code_to_name(user_data["equipes"])

    payload = {
	    "iat": datetime.utcnow(),
	    "nbf": datetime.utcnow(),
	    "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS),
	    "iss": "NRCan",
        "sub": "1234567890",
        "nom_usager": user_data["nom_usager"],
	    "scope": user_data["scopes"],
        "scope_nom": scopes_nom,
        "theme": user_data["themes"],
        "theme_nom": themes_nom,
        "equipes": user_data["equipes"],
        "equipes_nom": equipes_nom,
        "aws_access": user_data["cle_aws"]
    }

    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    
    # Construction de la reponse de retour
    reponse = SecuriteReponseLogin( access_token=jwt_token.decode(), #La serialization en JSON n'accepte pas les bytes
                                    token_type="Bearer",
                                    expires_in=JWT_EXP_DELTA_SECONDS,
                                    scope=user_data["scopes"],
                                    theme=user_data["themes"],
                                    equipe=user_data["equipes"],
                                    )
    
    return reponse


def get_securite_usager_nom(nom):  # noqa: E501
    """get_securite_usager_nom

     # noqa: E501

    :param nom: 
    :type nom: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def post_securite_usager(body=None):  # noqa: E501
    """post_securite_usager

    Ajouter un nouvel usager de l&#x27;API GeoSys. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    if connexion.request.is_json:
        body = Usager.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
