#!/usr/bin/env python3

'''
Created on 12 Oct 2018

@author: thomaspilz

"""
Very simple HTTP server in python.
Usage::
    ./server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
'''

# curl --header "Content-Type: application/json" --request POST --data '{"name":"test_user","slots": [["2018-10-12 10:00:00", "2018-10-12 11:00:00"]]}' http://localhost:8081

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from storage.storage_factory import StorageFactory


class JSONHandler(object):

    def prepare_data(self, request_data):
        try:
            return json.loads(request_data)
        except ValueError:
            return None


class RequestHandler(BaseHTTPRequestHandler):
    '''
    provides a simple REST-API-Interface
    @return response in JSON-Format
    '''

    CONTENT_TYPE_MAPPING = {'json': JSONHandler}

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def _extract_query_params(self):
        query_components = parse_qs(urlparse(self.path).query)
        return query_components

    def do_GET(self, *args):
        query_params = self._extract_query_params()
        name = None
        if 'name' in query_params:
            name = query_params.get('name')[0]
        if name:
            rtv = self.server.storage.get_slots_by_name(name)
        else:
            rtv = self.server.storage.get_all_slots()

        self._set_headers()
        self.wfile.write(b"<html><body><h1>Hello World</h1>")
        if rtv:
            for value in rtv:
                s = str.encode("<p>%s</p>" % str(value))
                self.wfile.write(s)
        self.wfile.write(b"</body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self, **kwds):
        post_data = self.rfile.read(int(self.headers['Content-Length']))
        content_type = self.headers.get('Content-Type')
        # handle different content_types
        if 'application/json' in content_type:
            _type = 'json'

        handler = self.CONTENT_TYPE_MAPPING.get(_type)
        data = handler.read_data(post_data)
        if data is None:
            self.send_response(404)
        else:
            self.send_response(200)

        #put either free slot by interviewer
        self.server.storage.set_slots_by_name(data.get('name'), data.get('slots'))
        #else put slot request by candidate
        self._set_headers()
        self.wfile.write(b"<html><body><h1>POST!</h1></body></html>")


class MyHTTPServer(HTTPServer):

    def __init__(self, server_address, RequestHandler, storage):
        HTTPServer.__init__(self, server_address, RequestHandler)
        self.storage = storage


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    # currently it's an in-memory storage
    # e.g. you could add a storage class for any DB backend
    storage = StorageFactory('slot_pool').create_storage()

    httpd = MyHTTPServer(server_address, RequestHandler, storage)
    print('running server...')
    try:
        # Listen for requests indefinitely
        httpd.serve_forever()
    except KeyboardInterrupt:
        # A request to terminate has been received, stop the server
        print("\nShutting down server...")
        httpd.socket.close()

run()
