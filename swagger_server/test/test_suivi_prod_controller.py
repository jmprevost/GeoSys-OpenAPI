# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.general_liste_valeur import GeneralListeValeur  # noqa: E501
from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.suivi_prod_code import SuiviProdCode  # noqa: E501
from swagger_server.models.suivi_prod_code_list import SuiviProdCodeList  # noqa: E501
from swagger_server.models.suivi_prod_etape_ut import SuiviProdEtapeUt  # noqa: E501
from swagger_server.models.suivi_prod_featuretype import SuiviProdFeaturetype  # noqa: E501
from swagger_server.models.suivi_prod_lot_no_rel import SuiviProdLotNoRel  # noqa: E501
from swagger_server.models.suivi_prod_planification import SuiviProdPlanification  # noqa: E501
from swagger_server.models.suivi_prod_unite_travail2_no_rel import SuiviProdUniteTravail2NoRel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSuiviProdController(BaseTestCase):
    """SuiviProdController integration test stubs"""

    def test_delete_suivi_prod_etape_ut_id(self):
        """Test case for delete_suivi_prod_etape_ut_id

        
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/etape-ut/{identifiant}'.format(identifiant='identifiant_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_suivi_prod_featuretype_id(self):
        """Test case for delete_suivi_prod_featuretype_id

        
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/featuretype/{identifiant}'.format(identifiant='identifiant_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_suivi_prod_lot_id(self):
        """Test case for delete_suivi_prod_lot_id

        
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/lot/{identifiant}'.format(identifiant='identifiant_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_suivi_prod_unite_travail_id(self):
        """Test case for delete_suivi_prod_unite_travail_id

        
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/unite-travail/{identifiant}'.format(identifiant='identifiant_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_code_list(self):
        """Test case for get_suivi_prod_code_list

        
        """
        query_string = [('id', 56),
                        ('nom', 'nom_example')]
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/codelist',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_codes(self):
        """Test case for get_suivi_prod_codes

        
        """
        query_string = [('categorie', 'categorie_example'),
                        ('nom', 'nom_example'),
                        ('id', 56),
                        ('id_list_codes', 56)]
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/codes',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_codes_code(self):
        """Test case for get_suivi_prod_codes_code

        
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/codes/{code}'.format(code='code_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_etape_ut_id(self):
        """Test case for get_suivi_prod_etape_ut_id

        Your GET endpoint
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/etape-ut/{identifiant}'.format(identifiant='identifiant_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_featuretype_id(self):
        """Test case for get_suivi_prod_featuretype_id

        Your GET endpoint
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/featuretype/{identifiant}'.format(identifiant='identifiant_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_lot_id(self):
        """Test case for get_suivi_prod_lot_id

        
        """
        query_string = [('full_relation', 'full_relation_example')]
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/lot/{identifiant}'.format(identifiant='identifiant_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_type_travail_theme(self):
        """Test case for get_suivi_prod_type_travail_theme

        Your GET endpoint
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/type-travail/theme/{theme}'.format(theme='theme_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_unite_travail_id(self):
        """Test case for get_suivi_prod_unite_travail_id

        
        """
        query_string = [('full_relation', true)]
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/unite-travail/{identifiant}'.format(identifiant='identifiant_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_suivi_prod_unite_travail_listeid_theme_actif(self):
        """Test case for get_suivi_prod_unite_travail_listeid_theme_actif

        Your GET endpoint
        """
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/unite-travail/id/theme/actif/{theme}'.format(theme='theme_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_suivi_prod_etape_ut(self):
        """Test case for post_suivi_prod_etape_ut

        
        """
        body = SuiviProdEtapeUt()
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/etape-ut',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_suivi_prod_featuretype(self):
        """Test case for post_suivi_prod_featuretype

        
        """
        body = [SuiviProdFeaturetype()]
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/featuretype',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_suivi_prod_lot(self):
        """Test case for post_suivi_prod_lot

        
        """
        body = SuiviProdLotNoRel()
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/lot',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_suivi_prod_planification(self):
        """Test case for post_suivi_prod_planification

        
        """
        body = SuiviProdPlanification()
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/planification',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_suivi_prod_unite_travail(self):
        """Test case for post_suivi_prod_unite_travail

        
        """
        body = SuiviProdUniteTravail2NoRel()
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/unite-travail',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_suivi_prod_etape_ut_id(self):
        """Test case for put_suivi_prod_etape_ut_id

        
        """
        body = SuiviProdEtapeUt()
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/etape-ut/{identifiant}'.format(identifiant='identifiant_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_suivi_prod_lot_id(self):
        """Test case for put_suivi_prod_lot_id

        
        """
        body = SuiviProdLotNoRel()
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/lot/{identifiant}'.format(identifiant='identifiant_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_suivi_prod_unite_travail_id(self):
        """Test case for put_suivi_prod_unite_travail_id

        
        """
        body = SuiviProdUniteTravail2NoRel()
        response = self.client.open(
            '/geosys-api/v1/suivi-prod/unite-travail/{identifiant}'.format(identifiant='identifiant_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
