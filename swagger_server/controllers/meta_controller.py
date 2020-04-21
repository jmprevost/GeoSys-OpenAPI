import connexion
import six

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.metadata_creation import MetadataCreation  # noqa: E501
from swagger_server import util


def post_geosys_creer_md(body=None):  # noqa: E501
    """post_geosys_creer_md

    Service intégrateur pour la création de métadonnées dans GeoSys. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: GeneralMessage
    """
    if connexion.request.is_json:
        body = MetadataCreation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_geosys_valider_md(theme=None, id_ut=None, fichier_json=None, logfile=None):  # noqa: E501
    """post_geosys_valider_md

    Service intégrateur pour la validation d&#x27;un fichier de métadonnées. # noqa: E501

    :param theme: 
    :type theme: str
    :param id_ut: 
    :type id_ut: str
    :param fichier_json: 
    :type fichier_json: strstr
    :param logfile: 
    :type logfile: str

    :rtype: GeneralMessage
    """
    return 'do some magic!'
