from geoalchemy2.elements import WKBElement
#from shapely_geojson import dumps, Feature
#from geoalchemy2.shape import to_shape
from sqlalchemy.sql import text
import json
import os

from swagger_server.utils import erreurs
from swagger_server.utils import utils_gapi
from swagger_server.config import db

def validate_geometry( geojson ):
    """validate_geometry

    Validation de la géométrie pour qu'elle soit conforme à la table unite_travail_2 du suivi de production.
    La fonction retourne un geoJSON validé et reprojté.

    :param geojson: Géométrie en GeoJSON
    :type geojson: str
    
    :rtype: str
    """
    try:
        # Verification si la geometrie repond au specs OGC. Verification avant la reprojection
        sql = "SELECT ST_IsValidReason(ST_GeomFromGeoJSON(:geom))"
        row = db.engine.execute(text(sql), geom = geojson).fetchone()    
        if str(row[0]).upper() != "VALID GEOMETRY":        
            raise erreurs.GAPIInvalidGeometry(str(row[0]))
        
        # Reprojection du GeoJSON en Lat/Long EPSG:4216
        # Forcer l'orientation des vertex du polygone selon le Right-Hand-Rule. 
        # Pour l'instant, nous utilisons PostGIS 2.3.7 et la fonction ST_ForceRHR qui ne donne pas des résultats intéressants.
        # Cepemndant, à partir de la versin 2.4 nous devrions utiliser la fonction ST_ForcePolygonCW qui est plus prometteuse.
        sql = "SELECT ST_AsGeoJSON(ST_Reverse(ST_Transform(ST_GeomFromGeoJSON(:geom), :epsg)), :max_decimal, :pgis_option)"
        row = db.engine.execute(    text(sql), 
                                    geom=geojson, 
                                    epsg=int(os.environ.get("GAPI_EPSG")), 
                                    max_decimal=int(os.environ.get("GAPI_GEOJSON_MAX_DECIMAL")), 
                                    pgis_option=int(os.environ.get("GAPI_GEOJSON_PGIS_OPTION"))).fetchone()
        reproj_geojson = str(row[0])

        # Verification si la geometrie repond au specs OGC. Verification apres la reprojection
        sql = "SELECT ST_IsValidReason(ST_GeomFromGeoJSON(:geom))"
        row = db.engine.execute(text(sql), geom = reproj_geojson).fetchone()
        if str(row[0]).upper() != "VALID GEOMETRY":
            raise erreurs.GAPIInvalidGeometry(str(row[0]))
        
        # Verification du nombre de polygone. Il doit y en avoir un seul
        sql = "SELECT ST_NumGeometries(ST_GeomFromGeoJSON(:geom))"
        row = db.engine.execute(text(sql), geom = reproj_geojson).fetchone() 
        if int(row[0]) != 1:
            raise erreurs.GAPIMultiPolygonNotAllowed(str(row[0]))

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))
    
    return reproj_geojson

def convert_geojson_to_wkt( geojson ):
    """convert_geojson_to_wkt

    Cette fonction convertit un GeoJSON en WKT.

    :param geojson: Géométrie en GeoJSON
    :type geojson: str
    
    :rtype: str
    """

    try:
        sql = "SELECT ST_AsText(ST_GeomFromGeoJSON(:geom))"
        row = db.engine.execute(text(sql), geom = geojson).fetchone()

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))

    return str(row[0])

def convert_whatever_to_geojson( geometrie ):
    """convert_whatever_to_geojson

    Cette fonction convertit un WKBElement, WKT ou EWKT en GeoJSON.

    :param geometrie: Géométrie à convertir
    :type geometrie: WKBElement, WKT ou EWKT
    
    :rtype: str
    """

    try:        
        if isinstance(geometrie, WKBElement):
            
            geojson = db.session.scalar(geometrie.ST_AsGeoJSON(int(os.environ.get("GAPI_GEOJSON_MAX_DECIMAL")), 
                                                               int(os.environ.get("GAPI_GEOJSON_PGIS_OPTION"))))
            
            return json.loads(geojson)

        elif isinstance(geometrie, str):
            g = str(geometrie).upper()
            if g.startswith("SRID"):
                sql = "SELECT ST_AsGeoJSON(ST_GeomFromEWKT(:geom), :max_decimal, :pgis_option)"
            elif g.startswith("POLYGON"):
                sql = "SELECT ST_AsGeoJSON(ST_GeomFromWKT(:geom), :max_decimal, :pgis_option)"
            else:
                raise erreurs.GAPIInvalidGeometry(geometrie)

            row = db.engine.execute(text(sql), geom = geometrie, 
                                               max_decimal=int(os.environ.get("GAPI_GEOJSON_MAX_DECIMAL")), 
                                               pgis_option=int(os.environ.get("GAPI_GEOJSON_PGIS_OPTION"))).fetchone()
            return json.loads(str(row[0]))
        
        else:
            raise erreurs.GAPIInvalidGeometry(str(geometrie))            

    except Exception as e:
        raise Exception(utils_gapi.message_erreur(e, 400))