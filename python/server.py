from wsgiref.simple_server import make_server
from wsgiref.util import application_uri, request_uri
import urlparse

import pagemaker
import apireader
from linkmodel import Link
from dbdumper import fetch_and_dump

PORT = 8663

def hello_world_app(environ, start_response):
    uri = request_uri(environ)
    uri = urlparse.urlparse(uri)
    
    if uri.path == '/':
        status = '200 OK' # HTTP Status
        headers = [('Content-type', 'text/html')] # HTTP Headers
        start_response(status, headers)
        links = Link.select_all()
        return pagemaker.make_page(links)
    if uri.path == '/fresh':
        status = '200 OK' # HTTP Status
        headers = [('Content-type', 'text/html')] # HTTP Headers
        start_response(status, headers)
        fetch_and_dump()
        links = Link.select_all()
        return pagemaker.make_page(links)
    start_response('404 Not Found', [('Content-type', 'text/html')])
    return ['<h1>404</h1>']

    
if __name__ == '__main__':
    httpd = make_server('', PORT, hello_world_app)
    print "Serving on port %d..." % PORT

    httpd.serve_forever()
