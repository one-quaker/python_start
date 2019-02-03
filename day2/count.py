import time


t = 2 * 3600
delay = 5


while t:
    print('Telegram bot, live coding starts in {:.02f} minutes 👍💪'.format(t / 60))
    t -= delay
    time.sleep(delay)

print('Start!!! 👍👍👍')
