from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from datetime import datetime
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


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


DATA = dict(result=list())
DATA_FP = os.path.join(ROOT_DIR, 'data.json')


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


def get_ts():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if not os.path.isfile(DATA_FP):
    write_conf([
        dict(id=0, first_name='John', last_name='Doe', salary=4000),
        dict(id=1, first_name='Jane', last_name='Doe', salary=5000),
    ], DATA_FP)


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
            DATA.update(dict(
                result=sorted(DATA.get('result'), key=lambda k: k['id']),
            ))
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


def update_data():
    while True:
        _data = read_conf(DATA_FP)
        for person in _data:
            if person not in DATA.get('result'):
                DATA['result'].append(person)
                DATA.update(dict(ts=get_ts()))
        for idx, i in enumerate(DATA.get('result')):
            if i not in _data:
                DATA['result'].pop(idx)
        time.sleep(5)


t1 = threading.Thread(target=run_webserver)
t1.start()

t2 = threading.Thread(target=update_data)
t2.start()
