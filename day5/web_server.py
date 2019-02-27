from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import datetime
import time
import argparse
import json
import os
import sys
import random
from pprint import pprint
import threading
import logging


parser = argparse.ArgumentParser(description='Web-server')
parser.add_argument('-H', '--host', type=str, default='0.0.0.0')
parser.add_argument('-P', '--port', type=int, default=8000)
parser.add_argument('-D', '--debug', action='store_true', default=False)
ARG = parser.parse_args()


WEB_HOST, WEB_PORT = ARG.host, ARG.port
LOG_TPL = '[%(levelname)s] %(message)s'
LOG_LEVEL = logging.DEBUG if ARG.debug else logging.INFO
logging.basicConfig(format=LOG_TPL, level=LOG_LEVEL)
log = logging.getLogger(__name__)


def write_conf(data, fp):
    with open(fp, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True)


def read_conf(fp):
    data = dict()
    try:
        with open(fp, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    return data


DATA = list()
DATA_FN = 'data.json'


if any((os.path.isfile(DATA_FN), not DATA)):
    write_conf([
        dict(first_name='John', last_name='Doe', salary=4000),
        dict(first_name='Jane', last_name='Doe', salary=5000),
    ], DATA_FN)
DATA = read_conf(DATA_FN)


class HttpRequestHandler(BaseHTTPRequestHandler):
    def _send_html(self, http_code, html):
        self.send_response(http_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def _send_json(self, d):
        try:
            res = json.dumps(d)
        except:
            self.send_response(500)
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(res.encode('utf-8'))

    def do_GET(self):
        if self.path == '/api/v1':
            self._send_json(DATA)
        else:
            self._send_html(200, '<h1>It works!</h1>')


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run_webserver():
    log.info('Starting server ...')
    log.info('Server listening on port {}:{} ...'.format(WEB_HOST, WEB_PORT))
    httpd = ThreadedHTTPServer((WEB_HOST, WEB_PORT), HttpRequestHandler)
    httpd.serve_forever()


run_webserver()
