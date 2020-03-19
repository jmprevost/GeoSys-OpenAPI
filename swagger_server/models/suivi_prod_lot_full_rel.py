# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.suivi_prod_lot_no_rel import SuiviProdLotNoRel  # noqa: F401,E501
from swagger_server.models.suivi_prodlotfull_rel_relation import SuiviProdlotfullRelRelation  # noqa: F401,E501
from swagger_server import util


class SuiviProdLotFullRel(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, lot: SuiviProdLotNoRel=None, relation: SuiviProdlotfullRelRelation=None):  # noqa: E501
        """SuiviProdLotFullRel - a model defined in Swagger

        :param lot: The lot of this SuiviProdLotFullRel.  # noqa: E501
        :type lot: SuiviProdLotNoRel
        :param relation: The relation of this SuiviProdLotFullRel.  # noqa: E501
        :type relation: SuiviProdlotfullRelRelation
        """
        self.swagger_types = {
            'lot': SuiviProdLotNoRel,
            'relation': SuiviProdlotfullRelRelation
        }

        self.attribute_map = {
            'lot': 'lot',
            'relation': 'relation'
        }
        self._lot = lot
        self._relation = relation

    @classmethod
    def from_dict(cls, dikt) -> 'SuiviProdLotFullRel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The suivi_prod-lot-full_rel of this SuiviProdLotFullRel.  # noqa: E501
        :rtype: SuiviProdLotFullRel
        """
        return util.deserialize_model(dikt, cls)

    @property
    def lot(self) -> SuiviProdLotNoRel:
        """Gets the lot of this SuiviProdLotFullRel.


        :return: The lot of this SuiviProdLotFullRel.
        :rtype: SuiviProdLotNoRel
        """
        return self._lot

    @lot.setter
    def lot(self, lot: SuiviProdLotNoRel):
        """Sets the lot of this SuiviProdLotFullRel.


        :param lot: The lot of this SuiviProdLotFullRel.
        :type lot: SuiviProdLotNoRel
        """

        self._lot = lot

    @property
    def relation(self) -> SuiviProdlotfullRelRelation:
        """Gets the relation of this SuiviProdLotFullRel.


        :return: The relation of this SuiviProdLotFullRel.
        :rtype: SuiviProdlotfullRelRelation
        """
        return self._relation

    @relation.setter
    def relation(self, relation: SuiviProdlotfullRelRelation):
        """Sets the relation of this SuiviProdLotFullRel.


        :param relation: The relation of this SuiviProdLotFullRel.
        :type relation: SuiviProdlotfullRelRelation
        """

        self._relation = relation
