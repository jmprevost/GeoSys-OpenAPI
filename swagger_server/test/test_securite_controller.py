# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.return_value_basic_error_message import ReturnValueBasicErrorMessage  # noqa: E501
from swagger_server.models.securite_reponse_login import SecuriteReponseLogin  # noqa: E501
from swagger_server.models.usager import Usager  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSecuriteController(BaseTestCase):
    """SecuriteController integration test stubs"""

    def test_delete_securite_usager_nom(self):
        """Test case for delete_securite_usager_nom

        
        """
        response = self.client.open(
            '/geosys-api/v1/securite/usager/{nom}'.format(nom='nom_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_securite_login(self):
        """Test case for get_securite_login

        
        """
        headers = [('usager', 'usager_example'),
                   ('mot_de_passe', 'mot_de_passe_example'),
                   ('duree_token', 56)]
        response = self.client.open(
            '/geosys-api/v1/securite/login',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_securite_usager_nom(self):
        """Test case for get_securite_usager_nom

        
        """
        response = self.client.open(
            '/geosys-api/v1/securite/usager/{nom}'.format(nom='nom_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_securite_usager(self):
        """Test case for post_securite_usager

        
        """
        body = Usager()
        response = self.client.open(
            '/geosys-api/v1/securite/usager',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
