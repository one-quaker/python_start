import argparse
import logging
import sys
import time


parser = argparse.ArgumentParser(description='Countdown timer')
parser.add_argument('-t', '--time', type=int, default=5, help='Time in seconds')
parser.add_argument('-d', '--delay', type=int, default=1, help='Delay in seconds')
parser.add_argument('-m', '--start-message', type=str, required=True, help='User message')
parser.add_argument('--test-float', type=float, help='Float test value')
parser.add_argument('--key-list', nargs='+', help='Key list')
parser.add_argument('--value-list', nargs='+', help='Value list')
parser.add_argument('-D', '--debug', action='store_true', default=False, help='Enable debug mode')


ARG = parser.parse_args()


LOG_TPL = '[%(levelname)s] %(message)s'
if ARG.debug:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
logging.basicConfig(format=LOG_TPL, level=LOG_LEVEL)
log = logging.getLogger()


# print(sys.argv)
# arg_name, arg_value = sys.argv[1].split('=')
# print(arg_name, arg_value)


t = ARG.time
delay = ARG.delay
BASE_TPL = 'Live coding starts in'


while t > 0:
    if t > 3600:
        log.debug(t / 3600)
        log.info('{0} {1} hours 👀'.format(BASE_TPL, round(t / 3600, 1)))
    elif t >= 60 and t <= 3600:
        log.info('{0} {1} minutes 👍💪'.format(BASE_TPL, int(t / 60)))
    else:
        log.info('{0} {1} seconds 👽'.format(BASE_TPL, t))
    t -= delay
    time.sleep(delay)
    log.debug('Delay: {}'.format(delay))
    log.debug('Time: {}'.format(t))


try:
    a = 8 / 0
except ZeroDivisionError:
    log.error('Division by zero. Go to school dude 😎👹😭')


log.debug(ARG.test_float)
log.debug('Debug mode ON')
log.warning(ARG.start_message)


data = dict()


for idx, key in enumerate(ARG.key_list):
    try:
        data[key] = ARG.value_list[idx]
    except IndexError:
        log.warning('Out of range')


log.info(data)
