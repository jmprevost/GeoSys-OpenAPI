# coding: utf-8

from swagger_server.config import db
from sqlalchemy.sql import text

from datetime import datetime

import jwt
import os

"""
from geoalchemy2.elements import WKBElement
from shapely_geojson import dumps, Feature
from geoalchemy2.shape import to_shape
import json
"""

import inspect
from tzlocal import get_localzone
from flask import make_response, jsonify
from swagger_server.controllers import suivi_prod_controller


def message_erreur(exception, code):
    """message_erreur:

    Cette fonction essaye de faire un message d'erreur standardisée... Il reste du travail à faire...

    :param exception: exception python
    :type exception: Exception
    :param code: code d'erreur REST
    :type code: int
    
    :rtype: response_class
    """
    
    stack_list = []
    for s in inspect.stack():
        if str(s.filename).find("swagger_server") > -1: # on ne conserve que les appels concerant le code de l'API
            # Chaque nouveau message est inséré au début de la liste
            stack_list[:0] = [(str("File '{}', line {}, in '{}'").format(s.filename, s.lineno, s.function))]
        else:
            break
    
    return make_response(jsonify(type_erreur=str(type(exception)),message=str(exception), stack=stack_list), code)

def convert_code_to_name( liste_code ):
    """convert_code_to_name:

    Extrait de la table "code" dans la BD de suivi de production le nom correspondant aux
    codes numériques passés en paramètre et retourne une nouvelle liste.

    :param liste_code: liste de code numérique
    :type liste_code: List[]
        
    :rtype: List[]
    """

    liste_nom = []
    for c in liste_code:
        ret = suivi_prod_controller.get_suivi_prod_codes_code(str(c))
        code = ret[0].get_json()
        liste_nom.append(code["nom"])
    
    return liste_nom

def date_now():
    """date_now:

    Retourne la date immédiate dans un format prédéfini.
        
    :rtype: str
    """

    return str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

def local_time_format( dt ):
    """local_time_format:

    Convertit le temps selon le fuseau du serveur hébergeant l'API Geosys
    
    :param dt: Date actuelle
    :type dt: datetime
        
    :rtype: datetime
    """
    
    format = "%Y-%m-%d %H:%M:%S"
    now_local = dt.astimezone(get_localzone())
    return now_local.strftime(format)
