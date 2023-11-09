import json
import unittest
import httpclient
import httpclienttest1
import tracemalloc

tracemalloc.start()

class TestHttpClient(httpclienttest1.TestHttpClient):
    
    def testPostMethod(self):
        client = httpclient.HttpClient('httpbin.org')
        response = client.doPost('/post', 'Foo=Bar')
        data = json.loads(response.body)
        self.assertEqual(data['form']['Foo'], 'Bar')
    
if __name__ == '__main__':
    unittest.main()
