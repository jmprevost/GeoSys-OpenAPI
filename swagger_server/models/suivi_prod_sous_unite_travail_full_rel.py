# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.suivi_prod_sous_unite_travail_no_rel import SuiviProdSousUniteTravailNoRel  # noqa: F401,E501
from swagger_server.models.suivi_prodsous_unite_travailfull_rel_relation import SuiviProdsousUniteTravailfullRelRelation  # noqa: F401,E501
from swagger_server import util


class SuiviProdSousUniteTravailFullRel(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, sous_unite_travail: SuiviProdSousUniteTravailNoRel=None, relation: SuiviProdsousUniteTravailfullRelRelation=None):  # noqa: E501
        """SuiviProdSousUniteTravailFullRel - a model defined in Swagger

        :param sous_unite_travail: The sous_unite_travail of this SuiviProdSousUniteTravailFullRel.  # noqa: E501
        :type sous_unite_travail: SuiviProdSousUniteTravailNoRel
        :param relation: The relation of this SuiviProdSousUniteTravailFullRel.  # noqa: E501
        :type relation: SuiviProdsousUniteTravailfullRelRelation
        """
        self.swagger_types = {
            'sous_unite_travail': SuiviProdSousUniteTravailNoRel,
            'relation': SuiviProdsousUniteTravailfullRelRelation
        }

        self.attribute_map = {
            'sous_unite_travail': 'sous_unite_travail',
            'relation': 'relation'
        }
        self._sous_unite_travail = sous_unite_travail
        self._relation = relation

    @classmethod
    def from_dict(cls, dikt) -> 'SuiviProdSousUniteTravailFullRel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The suivi_prod-sous_unite_travail-full_rel of this SuiviProdSousUniteTravailFullRel.  # noqa: E501
        :rtype: SuiviProdSousUniteTravailFullRel
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sous_unite_travail(self) -> SuiviProdSousUniteTravailNoRel:
        """Gets the sous_unite_travail of this SuiviProdSousUniteTravailFullRel.


        :return: The sous_unite_travail of this SuiviProdSousUniteTravailFullRel.
        :rtype: SuiviProdSousUniteTravailNoRel
        """
        return self._sous_unite_travail

    @sous_unite_travail.setter
    def sous_unite_travail(self, sous_unite_travail: SuiviProdSousUniteTravailNoRel):
        """Sets the sous_unite_travail of this SuiviProdSousUniteTravailFullRel.


        :param sous_unite_travail: The sous_unite_travail of this SuiviProdSousUniteTravailFullRel.
        :type sous_unite_travail: SuiviProdSousUniteTravailNoRel
        """

        self._sous_unite_travail = sous_unite_travail

    @property
    def relation(self) -> SuiviProdsousUniteTravailfullRelRelation:
        """Gets the relation of this SuiviProdSousUniteTravailFullRel.


        :return: The relation of this SuiviProdSousUniteTravailFullRel.
        :rtype: SuiviProdsousUniteTravailfullRelRelation
        """
        return self._relation

    @relation.setter
    def relation(self, relation: SuiviProdsousUniteTravailfullRelRelation):
        """Sets the relation of this SuiviProdSousUniteTravailFullRel.


        :param relation: The relation of this SuiviProdSousUniteTravailFullRel.
        :type relation: SuiviProdsousUniteTravailfullRelRelation
        """

        self._relation = relation
