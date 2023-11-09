import unittest
import json
from json import loads
import tracemalloc

tracemalloc.start()

import httpclient
import httpclienttest2

class TestHttpClient(httpclienttest2.TestHttpClient):

    def testPostWithParams(self):
        client = httpclient.HttpClient('httpbin.org')
        response = client.doPostWithParams('/post', {'Foo' : 'Bar'})
        data = json.loads(response.body)
        self.assertEqual(data['form']['Foo'], 'Bar')

    
    def testGetWithParams(self):
        client = httpclient.HttpClient('httpbin.org')
        response = client.doGetWithParams('/get', {'Foo' : 'Bar', 'foo' : 'bar'})
        data = json.loads(response.body)
        self.assertEquals(data['args'], {'Foo' : 'Bar', 'foo' : 'bar'})
    
if __name__ == '__main__':
    unittest.main()
