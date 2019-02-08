import argparse
import logging
import time


parser = argparse.ArgumentParser(description='Countdown timer')
parser.add_argument('-t', '--time', type=int, default=5, help='Time in seconds')
parser.add_argument('-d', '--delay', type=int, default=1, help='Delay in seconds')
parser.add_argument('-m', '--start-message', type=str, required=True, help='User message')
parser.add_argument('-D', '--debug', action='store_true', default=False, help='Enable debug mode')


ARG = parser.parse_args()


LOG_TPL = '[%(levelname)s] %(message)s'
if ARG.debug:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
logging.basicConfig(format=LOG_TPL, level=LOG_LEVEL)
log = logging.getLogger()


t = ARG.time
delay = ARG.delay
BASE_TPL = f'{ARG.start_message} starts in'


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


print('Start!!! 👍')
