
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
from swagger_server.controllers import utils_gapi
from flask import jsonify, request
from sqlalchemy.sql import text
import json
import boto3
import os

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

    token_dict = utils_gapi.auth_header_to_dict(request.headers.get('Authorization'))

    token_dict["aws_access"]["acces_id"]
    token_dict["aws_access"]["acces_secret"]

    s3_resource = boto3.resource(
        "s3",
        region_name = os.environ.get("GAPI_AWS_REGION"),
        aws_access_key_id = token_dict["aws_access"]["acces_id"],
        aws_secret_access_key = token_dict["aws_access"]["acces_secret"]
    )

    my_bucket = s3_resource.Bucket("mytestjmp")
    #summaries = my_bucket.objects.all()

    for obj in my_bucket.objects.all():
        print(obj.key)
    
    print("*************")

    for obj in my_bucket.objects.all():
        subsrc = obj.Object()
        print(obj.key, obj.storage_class, obj.last_modified,
            subsrc.version_id, subsrc.metadata, obj.size)

    print("*************")

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
    
    
    return 'Do some magic!!!'
