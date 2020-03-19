import connexion
import six

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.return_value_basic_error_message import ReturnValueBasicErrorMessage  # noqa: E501
from swagger_server.models.systeme_envs import SystemeEnvs  # noqa: E501
from swagger_server.models.systeme_liste_contenants_fichiers import SystemeListeContenantsFichiers  # noqa: E501
from swagger_server.models.systeme_ress_requete import SystemeRessRequete  # noqa: E501
from swagger_server.models.systeme_ress_retour import SystemeRessRetour  # noqa: E501
from swagger_server import util

# Ajouter manuellement
from swagger_server.config import db_view_session
from flask import jsonify, request
from sqlalchemy.sql import text
import json

def delete_systeme_contenants(contenant_url):  # noqa: E501
    """delete_systeme_contenants

    Efface un contenant (bucket) et les fichiers qu&#x27;il contient. # noqa: E501

    :param contenant_url: URL identifiant le contenant.
    :type contenant_url: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def delete_systeme_fichier(fichier_url):  # noqa: E501
    """delete_systeme_fichier

    Efface un fichier. # noqa: E501

    :param fichier_url: Chemin complet du fichier.
    :type fichier_url: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def get_systeme_envs():  # noqa: E501
    """get_systeme_envs

    Retourne la liste des environnements existant dans le système Geosys. # noqa: E501


    :rtype: SystemeEnvs
    """
    return 'do some magic!'


def get_systeme_fichier(fichier_url):  # noqa: E501
    """get_systeme_fichier

    Récupère un fichier # noqa: E501

    :param fichier_url: Chemin complet du fichier.
    :type fichier_url: str

    :rtype: str
    """
    return 'do some magic!'


def get_systeme_liste_contenants_fichiers(contenant_url):  # noqa: E501
    """get_systeme_liste_contenants_fichiers

    Renvoi la liste des fichiers et répertoires existants sous un URL donné dans Amazon S3. # noqa: E501

    :param contenant_url: 
    :type contenant_url: str

    :rtype: SystemeListeContenantsFichiers
    """
    return 'do some magic!'


def get_systeme_ressources(body=None, env=None):  # noqa: E501
    """get_systeme_ressources

    Retourne une ressource (paramètre ou un groupe de paramètres) à partir d&#x27;une liste de fichier. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param env: 
    :type env: str

    :rtype: SystemeRessRetour
    """
    if connexion.request.is_json:
        body = SystemeRessRequete.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_systeme_contenants(contenant_url):  # noqa: E501
    """post_systeme_contenants

    Création d&#x27;un contenant (bucket) pour le stockage de fichiers. # noqa: E501

    :param contenant_url: URL identifiant le contenant.
    :type contenant_url: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'


def post_systeme_fichier(fichier_url, body=None):  # noqa: E501
    """post_systeme_fichier

    Téléverser un fichier. # noqa: E501

    :param fichier_url: Chemin complet du fichier.
    :type fichier_url: str
    :param body: 
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    
    requete = """select 
                    lot.id, 
                    lot.theme_cl, 
                    code.nom, 
                    lot.statut_lot_cl, 
                    unite_travail_2.id as id_ut, 
                    unite_travail_2.shape 
                from 
                    lot, 
                    unite_travail_2,
                    code 
                where 
                        lot.theme_cl = 10307 
                    and lot.id = unite_travail_2.id_lot 
                    and lot.theme_cl = code.id"""
                    
    sql_json_template="""SELECT 
            COALESCE(json_agg(inputs), '[]'::json)
               FROM (
            ) inputs"""

    sql_geojson_template = """SELECT jsonb_build_object( 
            'type',     'FeatureCollection', 
            'features', jsonb_agg(feature) 
            ) 
            FROM ( 
            SELECT jsonb_build_object( 
                'type',       'Feature', 
                'geometry',   ST_AsGeoJSON(ST_Reverse(ST_Simplify(shape, 0.000005, True)),7,2)::json, 
                'properties', to_jsonb(inputs) - 'shape' 
            ) AS feature 
            FROM (  {} 
            ) inputs 
            ) features"""
    
    body_dict = json.loads(body.decode("utf-8"))
    sql_geojson_template = sql_geojson_template.format(body_dict['sql'])
    #print(sql_template)
    row = db_view_session.execute(text(sql_geojson_template)).fetchone()    
    #print (str(row[0]))

    return jsonify(row[0]), 200
    #return 'Do some magic!!!'
