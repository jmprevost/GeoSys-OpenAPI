
import connexion
import six

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.return_value_basic_error_message import ReturnValueBasicErrorMessage  # noqa: E501
from swagger_server.models.systeme_envs import SystemeEnvs  # noqa: E501
from swagger_server.models.systeme_envs_envs import SystemeEnvsEnvs  # noqa: E501
from swagger_server.models.systeme_liste_contenants_fichiers import SystemeListeContenantsFichiers  # noqa: E501
from swagger_server.models.systeme_liste_contenants_fichiers_list_file import SystemeListeContenantsFichiersListFile  # noqa: F401,E501
from swagger_server.models.systeme_liste_contenants_fichiers_list_folder import SystemeListeContenantsFichiersListFolder  # noqa: F401,E501
from swagger_server.models.systeme_ress_requete import SystemeRessRequete  # noqa: E501
from swagger_server.models.systeme_ress_retour import SystemeRessRetour  # noqa: E501
from swagger_server import util

# Ajouter manuellement
from swagger_server.utils import utils_s3
from swagger_server.utils import utils_gapi
from flask import jsonify, request, Response
from sqlalchemy.sql import text
import json
import boto3
import os
from werkzeug.utils import secure_filename

def delete_systeme_contenants(contenant_url):  # noqa: E501
    """delete_systeme_contenants

    Efface un contenant (bucket) et les fichiers qu'il contient. # noqa: E501

    :param contenant_url: URL identifiant le contenant.
    :type contenant_url: str

    :rtype: GeneralMessage
    """
    contenant_url = utils_s3.check_bucket_trailing_slash(contenant_url)
    
    s3_session = utils_s3.get_s3_session(contenant_url)
    s3_ress = s3_session.resource("s3")

    utils_s3.check_s3_obj_existance(s3_session.client("s3"), contenant_url)

    # Efface le répertoire ainsi que les sous-répertoires et fichiers
    bucket = s3_ress.Bucket(os.environ.get("GAPI_AWS_S3_BUCKET_NAME"))
    result = bucket.objects.filter(Prefix=contenant_url).delete()

    return jsonify(result), 200


def delete_systeme_fichier(fichier_url):  # noqa: E501
    """delete_systeme_fichier

    Efface un fichier. # noqa: E501

    :param fichier_url: Chemin complet du fichier.
    :type fichier_url: str

    :rtype: GeneralMessage
    """

    s3_session = utils_s3.get_s3_session(fichier_url)
    s3_client = s3_session.client("s3")

    utils_s3.check_s3_obj_existance(s3_client, fichier_url)

    result = s3_client.delete_object(Bucket=os.environ.get("GAPI_AWS_S3_BUCKET_NAME"), Key=fichier_url)
    
    return jsonify(result), 200


def get_systeme_envs():  # noqa: E501
    """get_systeme_envs

    Retourne la liste des environnements existant dans le système Geosys. # noqa: E501


    :rtype: SystemeEnvs
    """
    liste_envs = []
    liste_envs.append(SystemeEnvsEnvs(env="PRO", url="http://132.156.9.78:8080/geosys-api/v1/"))
    liste_envs.append(SystemeEnvsEnvs(env="TST", url="http://132.156.9.78:8080/geosys-api/v1/"))
    liste_envs.append(SystemeEnvsEnvs(env="DEV", url="http://132.156.9.78:8080/geosys-api/v1/"))
    
    return jsonify(SystemeEnvs(envs=liste_envs).to_dict()), 200


def get_systeme_fichier(fichier_url):  # noqa: E501
    """get_systeme_fichier

    Récupère un fichier # noqa: E501

    :param fichier_url: Chemin complet du fichier.
    :type fichier_url: str

    :rtype: str
    """
    # Check si le URL existe
    s3_session = utils_s3.get_s3_session(fichier_url)
    s3_client = s3_session.client("s3")

    # Extraire le nom du fichier
    parts = fichier_url.split("/")
    nom_fichier = parts[len(parts)-1]

    return Response(
        utils_s3.get_s3_object(s3_client, fichier_url),
        mimetype='application/octet-stream',
        headers={"Content-Disposition": "attachment;filename={}".format(nom_fichier)}
    )
    


def get_systeme_liste_contenants_fichiers(contenant_url=None):  # noqa: E501
    """get_systeme_liste_contenants_fichiers

    Renvoi la liste des fichiers et répertoires existants sous un URL donné dans Amazon S3. # noqa: E501

    :param contenant_url: 
    :type contenant_url: str

    :rtype: SystemeListeContenantsFichiers
    """

    # Si contenant_url est null ou égale à "/", ça veut dire que l'on veut lister la racine du bucket.
    # Alors on remplace la valeur de contenant_url par une chaine vide
    if str(contenant_url).strip() == "/" or contenant_url == None:
        contenant_url = ""
    
    contenant_url = utils_s3.check_bucket_trailing_slash(contenant_url)
    s3_session = utils_s3.get_s3_session(contenant_url)

    s3_client = s3_session.client("s3")
    s3_ress = s3_session.resource("s3")
    
    # Requête vers S3    
    result = s3_client.list_objects_v2(Bucket=os.environ.get("GAPI_AWS_S3_BUCKET_NAME"), Prefix=contenant_url, Delimiter='/')
    
    #Vérifie si le URL est bon
    if result.get('KeyCount') == 0:
        raise Exception(utils_gapi.message_erreur("Le URL: {} n'existe pas".format(contenant_url), 400))
    
    # Construction des listes des fichiers et des dossiers
    file_list = []
    folder_list = []
    
    if 'CommonPrefixes' in result: # S'il y a des dossiers
        for d in result.get('CommonPrefixes'):
            obj = s3_ress.Object(bucket_name=os.environ.get("GAPI_AWS_S3_BUCKET_NAME"), key=d.get('Prefix')) #Pour obtenir la date du dossier      
            folder_list.append(SystemeListeContenantsFichiersListFolder(name = str(d.get('Prefix')).replace(contenant_url,"").rstrip("/"),
                                                                        last_modified = utils_gapi.local_time_format(obj.last_modified)))
        
    if result.get('KeyCount') > 1 and 'Contents' in result : # S'il y a des fichiers
        for d in result.get('Contents'):
            if d["Key"] != contenant_url: #sinon on aura le nom du répertoire racine dans la liste
                file_list.append(SystemeListeContenantsFichiersListFile(name = str(d["Key"]).replace(contenant_url,""), 
                                                                        size = d["Size"], 
                                                                        last_modified = utils_gapi.local_time_format(d["LastModified"])))

    content_list = SystemeListeContenantsFichiers(list_file=file_list, list_folder=folder_list)

    return jsonify(content_list.to_dict()), 200


def post_systeme_contenants(contenant_url):  # noqa: E501
    """post_systeme_contenants

    Création d&#x27;un contenant (bucket) pour le stockage de fichiers. # noqa: E501

    :param contenant_url: URL identifiant le contenant.
    :type contenant_url: str

    :rtype: GeneralMessage
    """
    contenant_url = utils_s3.check_bucket_trailing_slash(contenant_url)
    ret = utils_s3.create_s3_object(contenant_url)

    # Retour    
    return jsonify(GeneralMessage(message=ret).to_dict()), 200


def post_systeme_fichier(contenant_url, fichier=None):  # noqa: E501
    """post_systeme_fichier

    Téléverser un fichier. # noqa: E501

    :param contenant_url: Chemin complet du fichier.
    :type contenant_url: str
    :param fichier: 
    :type fichier: strstr

    :rtype: GeneralMessage
    """
    
    contenant_url = utils_s3.check_bucket_trailing_slash(contenant_url)
    ret = utils_s3.create_s3_object(contenant_url, fichier)

    # Retour    
    return jsonify(GeneralMessage(message=ret).to_dict()), 200

def post_systeme_ressources_recherche(body=None, env=None):  # noqa: E501
    """post_systeme_ressources_recherche

    Retourne une ressource (paramètre ou un groupe de paramètres) à partir d&#x27;une liste de fichier. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param env: 
    :type env: str

    :rtype: SystemeRessRetour
    """
    #if connexion.request.is_json:
    #    body = SystemeRessRequete.from_dict(connexion.request.get_json())  # noqa: E501

    ret = {"value":{"liste_classe":["waterbody_2", "water_linear_flow_1", "dam_2"]}}

    return jsonify(ret), 200
