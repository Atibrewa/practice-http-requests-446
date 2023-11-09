import socket
import string
#import urllib
import urllib.parse

class HttpResponse:
    """
        Holds a structured http response.
        You will be responsible for translating an http response
        string into this structure.
    """
    def __init__(self):
        self.statusCode = 200
        self.statusMessage = 'OK'
        self.headers = {}
        self.body = ''
    
    def __repr__(self):
        return (
                'status=%s headers=%s body=%s...' %
                (self.statusCode, self.headers, self.body)
            )
        
class HttpClient:
    def __init__(self, host, port=80):
        """Constructs a new http client."""
        self.host = host
        self.port = port
    
    def doGet(self, path):
        """
            Executes an HTTP GET method and returns the result
            as an HttpResponse object.
        """
        sock = self._writeRequest(self._constructGetRequest(path))
        return self._readResponse(sock)
        
    def doPost(self, path, body):
        """
            Executes an HTTP POST method and returns the result
            as an HttpResponse object.
        """
        sock = self._writeRequest(self._constructPostRequest(path, body))
        return self._readResponse(sock)
    
    def doGetWithParams(self, path, params):
        """
            Executes an HTTP GET method and returns the result
            Params should be a dictionary of unencoded query parameters
            as an HttpResponse object. Please enter code below.
        """
        newURL = path +"?"+ urllib.parse.urlencode(params)
        return self.doGet(newURL)
    
    def doPostWithParams(self, path, params):
        """
            Executes an HTTP POST method and returns the result
            Params should be a dictionary of unencoded query parameters
            as an HttpResponse object. Please enter code below.
        """
        newURL = path 
        body = urllib.parse.urlencode(params)
        return self.doPost(newURL, body)
    
    def _constructGetRequest(self, path):
        """
            Returns a string containing an HTTP 1.0 GET request
            for self.host and the requested path. Please enter code below.
        """
        return '\r\n'.join([
            "GET %s HTTP/1.0" %path,
            "Host: %s" %self.host,
            "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "",
            ""
        ])
    
    def _constructPostRequest(self, path, body):
        """
            Returns a string containing an HTTP 1.0 POST request
            for self.host and the requested path and body. Please enter code below.
        """
        x = str(len(body))
        return '\r\n'.join([
            "POST %s HTTP/1.0" %path,
            "Host: %s" %self.host,
            "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Content-Type: application/x-www-form-urlencoded",
            "Content-Length: %s" %x,
            "",
            "%s" %body,
            "",
            ""
        ])
    
    def _writeRequest(self, request):
        """
            Creates a socket connected to the host and port
            Writes the request out and returns the socket object.
        """
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(request.encode('utf-8'))
        return s
    
    def _readResponse(self, sock):
        """
            Reads in a response from a socket object.
            Returns a filled-in HttpResponse object.
        """
        responseLines = self._readResponseStr(sock).split('\r\n')
        print(responseLines)
        response = HttpResponse()
        
        # the member variables for the http response object
        # by parsing the responseLines list of strings
        
        for i, line in enumerate(responseLines):
            if i == 0:
                (version, code, reason) = line.split(' ', 2)
                response.statusCode = int(code)
                response.statusMessage = reason
            elif not line:
                response.body = '\r\n'.join(responseLines[i+1:])
                break
            else:
                key, value = line.split(':', 1)
                response.headers[key.strip()] = value.strip()
        
        return response 
    
    def _readResponseStr(self, sock):
        """
            Reads in a response from a socket object.
            Returns the string contents of the response.
        """
        # Reads the response.
        # Since we are using HTTP 1.0, we can read until EOF
        bytesRead = 'foo'
        response = ''        
        while len(bytesRead) > 0: 
            bytesRead = sock.recv(1024)
            response += bytesRead.decode('utf-8')
        return response    
    
if __name__ == '__main__':
    client1 = HttpClient('www.npr.org')
    print(client1.doGet('/index.html'))
    client1 = HttpClient('webapps.macalester.edu')
    print(client1.doPost('/directory/search.cfm', 'Name=kyle'))
