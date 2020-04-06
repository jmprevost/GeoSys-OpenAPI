# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class SystemeFichier(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, fichier: str=None):  # noqa: E501
        """SystemeFichier - a model defined in Swagger

        :param fichier: The fichier of this SystemeFichier.  # noqa: E501
        :type fichier: str
        """
        self.swagger_types = {
            'fichier': str
        }

        self.attribute_map = {
            'fichier': 'fichier'
        }
        self._fichier = fichier

    @classmethod
    def from_dict(cls, dikt) -> 'SystemeFichier':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The systeme_fichier of this SystemeFichier.  # noqa: E501
        :rtype: SystemeFichier
        """
        return util.deserialize_model(dikt, cls)

    @property
    def fichier(self) -> str:
        """Gets the fichier of this SystemeFichier.


        :return: The fichier of this SystemeFichier.
        :rtype: str
        """
        return self._fichier

    @fichier.setter
    def fichier(self, fichier: str):
        """Sets the fichier of this SystemeFichier.


        :param fichier: The fichier of this SystemeFichier.
        :type fichier: str
        """

        self._fichier = fichier
