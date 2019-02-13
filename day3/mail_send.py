import json
import time
import os
import sys
import argparse


CONF_FN = 'conf.json'
CONF_FP = os.path.join(os.getcwd(), CONF_FN)


parser = argparse.ArgumentParser(description='Email send')
parser.add_argument('-D', '--debug', action='store_true', default=False)
ARG = parser.parse_args()


def get_log(debug):
    import logging
    LOG_TPL = '[%(levelname)s] %(message)s'
    LOG_LEVEL = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format=LOG_TPL, level=LOG_LEVEL)
    log = logging.getLogger(__name__)
    return log


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


CONF = read_conf(CONF_FP)
log = get_log(ARG.debug)


if not os.path.isfile(CONF_FP) or not CONF:
    email_list = [
        'user1@gmail.com',
        'user2@gmail.com',
        'user3@gmail.com',
    ]
    message = dict(
        text='Message body text',
        subject='Message subject here'
    )
    write_conf(dict(email_list=email_list, message=message), CONF_FP)
    print(f'Please edit {CONF_FN}')
    sys.exit(1)


log.debug(CONF['message'])
