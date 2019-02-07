import argparse
import logging
import sys
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
log = logging.getLogger(__name__)


# print(sys.argv)
# arg_name, arg_value = sys.argv[1].split('=')
# print(arg_name, arg_value)


t = ARG.time
delay = ARG.delay


while t > 0:
    log.info('Live coding starts in {:.02f} minutes 👍💪'.format(t / 60))
    t -= delay
    time.sleep(delay)
    log.debug('Delay: {}'.format(delay))
    log.debug('Time: {}'.format(t))


log.warning(ARG.start_message)
log.error('Test error')
log.debug('Debug mode ON')
