# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.geodata_edition import GeodataEdition  # noqa: E501
from swagger_server.models.geodata_lecture import GeodataLecture  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDataController(BaseTestCase):
    """DataController integration test stubs"""

    def test_get_geodata(self):
        """Test case for get_geodata

        
        """
        body = GeodataLecture()
        headers = [('env_app', 'env_app_example')]
        response = self.client.open(
            '/geosys-api/v1/geodata',
            method='GET',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_geodata_identifiant(self):
        """Test case for get_geodata_identifiant

        
        """
        headers = [('env_app', 'env_app_example')]
        response = self.client.open(
            '/geosys-api/v1/geodata/{identifiant}'.format(identifiant='identifiant_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_geodata_identifiant(self):
        """Test case for post_geodata_identifiant

        
        """
        headers = [('env_app', 'env_app_example')]
        data = dict(fichier_data='fichier_data_example',
                    fichier_meta='fichier_meta_example')
        response = self.client.open(
            '/geosys-api/v1/geodata/{identifiant}'.format(identifiant='identifiant_example'),
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_geodata_identifiant(self):
        """Test case for put_geodata_identifiant

        
        """
        body = GeodataEdition()
        headers = [('env_app', 'env_app_example')]
        response = self.client.open(
            '/geosys-api/v1/geodata/{identifiant}'.format(identifiant='identifiant_example'),
            method='PUT',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
