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
import sys
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
    func = sys._getframe(1).f_code.co_name    
    module = inspect.stack()[1].filename

    return make_response(jsonify(type_erreur=str(type(exception)),message=str(exception), fonction_origine=func, fichier_origine=module ), code)

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

"""
def validate_geometry( geojson ):
    
    # Verification si la geometrie repond au specs OGC. Verification avant la reprojection
    sql = "SELECT ST_IsValidReason(ST_GeomFromGeoJSON(:geom))"
    row = db.engine.execute(text(sql), geom = geojson).fetchone()    
    if str(row[0]).upper() != "VALID GEOMETRY":        
        raise Exception("Geométrie invalide. {}".format(str(row[0])))
    
    # Reprojection du GeoJSON en Lat/Long EPSG:4216
    # Forcer l'orientation des vertex du polygone selon le Right-Hand-Rule. 
    # Pour l'instant, nous utilisons PostGIS 2.3.7 et la fonction ST_ForceRHR qui ne donne pas des résultats intéressants.
    # Cepemndant, à partir de la versin 2.4 nous devrions utiliser la fonction ST_ForcePolygonCW qui est plus prometteuse.
    sql = "SELECT ST_AsGeoJSON(ST_ForceRHR(ST_Transform(ST_GeomFromGeoJSON(:geom), :epsg)), :max_decimal, :pgis_option)"
    row = db.engine.execute(text(sql), geom=geojson, epsg=int(os.environ.get("GAPI_EPSG")), max_decimal=int(os.environ.get("GAPI_GEOJSON_MAX_DECIMAL")), pgis_option=int(os.environ.get("GAPI_GEOJSON_PGIS_OPTION"))).fetchone()
    reproj_geojson = str(row[0])

    # Verification si la geometrie repond au specs OGC. Verification apres la reprojection
    sql = "SELECT ST_IsValidReason(ST_GeomFromGeoJSON(:geom))"
    row = db.engine.execute(text(sql), geom = reproj_geojson).fetchone()
    if str(row[0]).upper() != "VALID GEOMETRY":
        raise Exception("Geométrie invalide. {}".format(str(row[0])))
    
    # Verification du nombre de polygone. Il doit y en avoir un seul
    sql = "SELECT ST_NumGeometries(ST_GeomFromGeoJSON(:geom))"
    row = db.engine.execute(text(sql), geom = reproj_geojson).fetchone() 
    if int(row[0]) != 1:
        raise Exception("Les multipolygones ne sont pas acceptés. Votre géométrie contient {} polygones".format(row[0]))

    return reproj_geojson
"""

"""
def auth_header_to_dict( auth_header ):
    auth_type, token = auth_header.split(None, 1)

    JWT_SECRET = os.environ.get("GAPI_CRYPTO_SALT")
    JWT_ALGORITHM = os.environ.get("GAPI_JWT_ALGORITHM")

    token_content = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

    return token_content
"""

"""
def convert_geojson_to_wkt( geojson ):

    sql = "SELECT ST_AsText(ST_GeomFromGeoJSON(:geom))"
    row = db.engine.execute(text(sql), geom = geojson).fetchone()
    return str(row[0])
"""

"""
def check_s3_theme_access( themes, s3_path ):
    
    parts = str(s3_path).split("/")
    if len(parts) >= 4:
        return set([parts[3]]).issubset(set(themes))
    else:
        return True
"""

"""
def convert_whatever_to_geojson( geometrie ):
    
    try:        
        if isinstance(geometrie, WKBElement):
            feature = Feature(to_shape(geometrie))
            geoJSON = json.loads(dumps(feature))
            
            # On insére la projection dans le GeoJSON
            epsg = "EPSG:{}".format(os.environ.get("GAPI_EPSG"))
            geoJSON["crs"] = {'type':'name','properties':{'name':epsg}}
            
            return geoJSON

        elif isinstance(geometrie, str):
            g = str(geometrie).upper()
            if g.startswith("SRID"):
                sql = "SELECT ST_AsGeoJSON(ST_GeomFromEWKT(:geom), :max_decimal, :pgis_option)"
            elif g.startswith("POLYGON"):
                sql = "SELECT ST_AsGeoJSON(ST_GeomFromWKT(:geom), :max_decimal, :pgis_option)"
            else:
                raise Exception("ERREUR: utils_gapi.convert_whatever_to_geojson() chaine de caractère inconnue: "+geometrie)

            row = db.engine.execute(text(sql), geom = geometrie, max_decimal=int(os.environ.get("GAPI_GEOJSON_MAX_DECIMAL")), pgis_option=int(os.environ.get("GAPI_GEOJSON_PGIS_OPTION"))).fetchone()
            return json.loads(str(row[0]))
        
        else:
            raise Exception("ERREUR: utils_gapi.convert_whatever_to_geojson() type de géométrie inconnue: "+str(geometrie))                

    except Exception as e:
        raise Exception(e)
"""