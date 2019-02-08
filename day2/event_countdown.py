import argparse
import logging
import time


def check_positive(val):
    val = int(val)
    if val <= 0:
        raise argparse.ArgumentTypeError(f'\"{val}\", need positive int value')
    return val


parser = argparse.ArgumentParser(description='Countdown timer')
parser.add_argument('-t', '--time', type=check_positive, default=5, help='Time in seconds')
parser.add_argument('-d', '--delay', type=check_positive, default=1, help='Delay in seconds')
parser.add_argument('-C', '--count-message', type=str, required=True, help='Count message')
parser.add_argument('-S', '--start-message', type=str, default='Start!!! 👍', help='Start message')
parser.add_argument('-D', '--debug', action='store_true', default=False, help='Enable debug mode')


ARG = parser.parse_args()


LOG_TPL = '[%(levelname)s] %(message)s'
if ARG.debug:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
logging.basicConfig(format=LOG_TPL, level=LOG_LEVEL)
log = logging.getLogger()


BASE_TPL = f'{ARG.count_message} starts in'


t = ARG.time
delay = ARG.delay
if delay > t:
    delay = t


while t > 0:
    if t >= 3600:
        log.debug(t / 3600)
        log.info('{0} {1} hours 👀'.format(BASE_TPL, round(t / 3600, 1)))
    elif 120 < t < 3600:
        log.info('{0} {1} minutes 💪'.format(BASE_TPL, int(t / 60)))
    else:
        log.warning('{0} {1} seconds 👽'.format(BASE_TPL, t))
    t -= delay
    time.sleep(delay)
    log.debug(f'Delay: {delay}')
    log.debug(f'Time: {t}')


print(ARG.start_message)
