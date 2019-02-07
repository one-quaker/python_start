import argparse
import logging
import sys
import time


# parser = argparse.ArgumentParser(description='Telegram bot')
# parser.add_argument('--to-stdout', action='store_true', default=False)
# parser.add_argument('--debug', action='store_true', default=False)
# ARG = parser.parse_args()


print(sys.argv)
arg_name, arg_value = sys.argv[1].split('=')
print(arg_name, arg_value)


t = 5 * 60
delay = 5


# while t:
#     print('Telegram bot, live coding starts in {:.02f} minutes 👍💪'.format(t / 60))
#     t -= delay
#     time.sleep(delay)

# print('Start!!! 👍👍👍')
