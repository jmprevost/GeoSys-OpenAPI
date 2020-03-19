# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.return_value_basic_error_message import ReturnValueBasicErrorMessage  # noqa: E501
from swagger_server.models.systeme_envs import SystemeEnvs  # noqa: E501
from swagger_server.models.systeme_liste_contenants_fichiers import SystemeListeContenantsFichiers  # noqa: E501
from swagger_server.models.systeme_ress_requete import SystemeRessRequete  # noqa: E501
from swagger_server.models.systeme_ress_retour import SystemeRessRetour  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSystemeController(BaseTestCase):
    """SystemeController integration test stubs"""

    def test_delete_systeme_contenants(self):
        """Test case for delete_systeme_contenants

        
        """
        query_string = [('contenant_url', 'contenant_url_example')]
        response = self.client.open(
            '/geosys-api/v1/systeme/contenants',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_systeme_fichier(self):
        """Test case for delete_systeme_fichier

        
        """
        query_string = [('fichier_url', 'fichier_url_example')]
        response = self.client.open(
            '/geosys-api/v1/systeme/fichiers',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_systeme_envs(self):
        """Test case for get_systeme_envs

        
        """
        response = self.client.open(
            '/geosys-api/v1/systeme/envs',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_systeme_fichier(self):
        """Test case for get_systeme_fichier

        
        """
        query_string = [('fichier_url', 'fichier_url_example')]
        response = self.client.open(
            '/geosys-api/v1/systeme/fichiers',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_systeme_liste_contenants_fichiers(self):
        """Test case for get_systeme_liste_contenants_fichiers

        
        """
        query_string = [('contenant_url', 'contenant_url_example')]
        response = self.client.open(
            '/geosys-api/v1/systeme/liste-contenants-fichiers',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_systeme_ressources(self):
        """Test case for get_systeme_ressources

        
        """
        body = SystemeRessRequete()
        headers = [('env', 'env_example')]
        response = self.client.open(
            '/geosys-api/v1/systeme/ressources',
            method='GET',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_systeme_contenants(self):
        """Test case for post_systeme_contenants

        
        """
        query_string = [('contenant_url', 'contenant_url_example')]
        response = self.client.open(
            '/geosys-api/v1/systeme/contenants',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_systeme_fichier(self):
        """Test case for post_systeme_fichier

        
        """
        body = Object()
        query_string = [('fichier_url', 'fichier_url_example')]
        response = self.client.open(
            '/geosys-api/v1/systeme/fichiers',
            method='POST',
            data=json.dumps(body),
            content_type='application/octet-stream',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
