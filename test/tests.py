"""
Regression type tests for the alteracloud API.

These perform comparisons against golden file patterns to ensure that
tests are passing and not failing.
"""

import unittest
import json
import os
from requests.compat import urljoin
import requests

import alteracloud

# Test server for HTTP to replicate 
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')

# Make sure the URL always has a trailing slash
HTTPBIN = HTTPBIN.rstrip('/') + '/'


class ApiTests(unittest.TestCase):

    altera_server = "https://cloud.altera.com"

    def httpbin(self, *suffix):
        """
        Returns url for HTTPBIN resource.
        """
        return urljoin(HTTPBIN, '/'.join(suffix))

    def test_get(self):
        c = alteracloud.AlteraApiConnection(self.httpbin('get'))
        resp, content = c.request_get('')
        self.assertEqual(resp.status, 200)

        # Test get with query params
        query_params = {'key1':'value1', 'key2':'value2'}
        resp, content = c.request_get('', params=query_params)
        self.assertEqual(resp.status, 200)
        # Make sure the url is correct
        qs = resp.url.split("?", 1)[1]
        # Since the encoding order appears to be random
        self.assertTrue(qs in ["key1=value1&key2=value2", "key2=value2&key1=value1"])

    def test_post(self):
        data = {'foo':'bar'}
        c = alteracloud.AlteraApiConnection(self.httpbin('post'))
        resp, content = c.request_post('', data=data)
        self.assertEqual(resp.status, 200) 
        self.assertEqual(json.loads(content)['json'], data)

    def test_put(self):
        data = {'foo':'bar'}
        c = alteracloud.AlteraApiConnection(self.httpbin('put'))
        resp, content = c.request_put('', data=data)
        self.assertEqual(resp.status, 200) 
        self.assertEqual(json.loads(content)['json'], data)     

    def test_patch(self):
        data = {'foo':'bar'}
        c = alteracloud.AlteraApiConnection(self.httpbin('patch'))
        resp, content = c.request_patch('', data=data)
        self.assertEqual(resp.status, 200) 
        self.assertEqual(json.loads(content)['json'], data)     

    def test_delete(self):
        c = alteracloud.AlteraApiConnection(self.httpbin('delete'))
        resp, content = c.request_delete('')        
        self.assertEqual(resp.status, 200)
        
    """
    Login tests
    """
    
    def test_invalid_login(self):
        c = alteracloud.AlteraApiConnection(self.altera_server)
        self.assertFalse(c.login("invaliduser", "badpass"))

    def test_valid_login(self):
        c = alteracloud.AlteraApiConnection(self.altera_server)
        self.assertTrue(c.login("testuser", "testpass"))

if __name__ == '__main__':
    unittest.main()






