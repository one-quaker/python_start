import json
import datetime
import os
import sys
import argparse
import logging
from collections import defaultdict
from pprint import pprint


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_FP = os.path.join(ROOT_DIR, 'result.json')


parser = argparse.ArgumentParser()
parser.add_argument('-D', '--debug', action='store_true', default=False)
ARG = parser.parse_args()


LOG_TPL = '[%(levelname)s] %(message)s'
LOG_LEVEL = logging.DEBUG if ARG.debug else logging.INFO
logging.basicConfig(format=LOG_TPL, level=LOG_LEVEL)
log = logging.getLogger(__name__)


def read_conf(fp):
    data = dict()
    try:
        with open(fp, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    return data


def write_conf(data, fp):
    with open(fp, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True)


def donate2usd(*arg, **kw):
    rate = dict(
        RUB=66,
        UAH=27,
        USD=1,
    )
    amount = kw['amount'].replace(',', '.')
    return float(amount) / rate[kw['currency']]


DATA = read_conf(RESULT_FP)


if any((not os.path.isfile(RESULT_FP), not DATA)):
    print(f'\"{RESULT_FP}\" not found or empty')
    sys.exit(1)


result = DATA.get('result', [])


subscriber_list = [x.get('user_name') for x in result if x.get('subscriber')]
donator_list = [(x.get('user_name'), donate2usd(**x.get('donation'))) for x in result if x.get('donation')]
top_donator = defaultdict(float)


for i in donator_list:
    top_donator[i[0]] += i[1]


if ARG.debug:
    print(result)
    print(donator_list)


print('Subscriber list:\n-----------------\n{}'.format('\n'.join(subscriber_list)))
print(32 * '=')
top_donator_total = sorted(top_donator.items(), key=lambda kv: kv[1], reverse=True)
print('\n'.join(['{}: {}$'.format(x[0], round(x[1], 2)) for x in top_donator_total]))
