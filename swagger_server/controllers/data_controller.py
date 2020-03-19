# coding: iso-8859-1
import connexion
import six

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.geodata_edition import GeodataEdition  # noqa: E501
from swagger_server.models.geodata_lecture import GeodataLecture  # noqa: E501
from swagger_server import util

#Ajouté manuellement
import os
from werkzeug.utils import secure_filename

def get_geodata(body=None):  # noqa: E501
    """get_geodata

    Extraction de donnée à sens unique. La donnée extraite ne reviendra pas. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    if connexion.request.is_json:
        body = GeodataLecture.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_geodata_identifiant(identifiant):  # noqa: E501
    """get_geodata_identifiant

     # noqa: E501

    :param identifiant: 
    :type identifiant: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'

def post_geodata_identifiant(identifiant, fichier_data=None, fichier_meta=None, env_app=None):  # noqa: E501
    """post_geodata_identifiant

     # noqa: E501

    :param identifiant: 
    :type identifiant: str
    :param fichier_data: 
    :type fichier_data: strstr
    :param fichier_meta: 
    :type fichier_meta: strstr
    :param env_app: 
    :type env_app: str

    :rtype: GeneralMessage
    """

    filename = secure_filename(fichier_data.filename)
    fichier_data.save(os.path.join('D:/GeoSys/out', filename))

    filename = secure_filename(fichier_meta.filename)
    fichier_meta.save(os.path.join('D:/GeoSys/out', filename))

    return 'do some magic!'

#def post_geodata_identifiant(identifiant, body=None):  # noqa: E501
    """post_geodata_identifiant

     # noqa: E501

    :param identifiant: 
    :type identifiant: str
    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    """   
    if connexion.request.is_json:
        body = GeodataEdition.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
    """

def put_geodata_identifiant(identifiant, fichier_data=None, fichier_meta=None, env_app=None):  # noqa: E501
    """put_geodata_identifiant

     # noqa: E501

    :param identifiant: 
    :type identifiant: str
    :param fichier_data: 
    :type fichier_data: strstr
    :param fichier_meta: 
    :type fichier_meta: strstr
    :param env_app: 
    :type env_app: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'

