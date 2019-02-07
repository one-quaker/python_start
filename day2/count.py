import argparse
import logging
import sys
import time


parser = argparse.ArgumentParser(description='Countdown timer')
parser.add_argument('-t', '--time', type=int, default=5, help='Time in seconds')
# parser.add_argument('--debug', action='store_true', default=False)
ARG = parser.parse_args()


# print(sys.argv)
# arg_name, arg_value = sys.argv[1].split('=')
# print(arg_name, arg_value)


t = ARG.time
delay = 5


while t:
    print('Telegram bot, live coding starts in {:.02f} minutes 👍💪'.format(t / 60))
    t -= delay
    time.sleep(delay)

print('Start!!! 👍👍👍')
