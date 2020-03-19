# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.general_message import GeneralMessage  # noqa: E501
from swagger_server.models.metadata_creation import MetadataCreation  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGeosysController(BaseTestCase):
    """GeosysController integration test stubs"""

    def test_post_geosys_creer_md(self):
        """Test case for post_geosys_creer_md

        
        """
        body = MetadataCreation()
        response = self.client.open(
            '/geosys-api/v1/geosys/creer-md',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_geosys_valider_md(self):
        """Test case for post_geosys_valider_md

        
        """
        data = dict(theme='theme_example',
                    id_ut='id_ut_example',
                    fichier_json='fichier_json_example',
                    logfile='logfile_example')
        response = self.client.open(
            '/geosys-api/v1/geosys/valider-md',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
