from wsgiref.simple_server import make_server
from wsgiref.util import application_uri, request_uri
import urlparse

import pagemaker
import apireader
from linkmodel import Link
from dbdumper import fetch_and_dump

def hello_world_app(environ, start_response):
    uri = request_uri(environ)
    uri = urlparse.urlparse(uri)
    
    if uri.path == '/pics':
        status = '200 OK' # HTTP Status
        headers = [('Content-type', 'text/html')] # HTTP Headers
        start_response(status, headers)
        links = Link.select_all()
        return pagemaker.make_page(links)
    if uri.path == '/pics/fresh':
        status = '200 OK' # HTTP Status
        headers = [('Content-type', 'text/html')] # HTTP Headers
        start_response(status, headers)
        fetch_and_dump()
        links = Link.select_all()
        return pagemaker.make_page(links)
    start_response('404 Not Found', [('Content-type', 'text/html')])
    return ['<h1>404</h1>']

httpd = make_server('', 8000, hello_world_app)
print "Serving on port 8000..."

httpd.serve_forever()