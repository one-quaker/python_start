import json
import time
import os
import sys
import argparse
import re
import urllib
import urllib.request
import random
from pprint import pprint


LAST_MSG_FN = 'last_msg.json'
LAST_MSG_FP = os.path.join(os.getcwd(), LAST_MSG_FN)
CONF_FN = 'conf.json'
CONF_FP = os.path.join(os.getcwd(), CONF_FN)


parser = argparse.ArgumentParser(description='Telegram bot')
parser.add_argument('--to-stdout', action='store_true', default=False)
parser.add_argument('--debug', action='store_true', default=False)
ARG = parser.parse_args()


CMD_HELP   = 'help'
CMD_INFO   = 'info'
CMD_HI     = 'hi'
CMD_HELLO  = 'hello'
CMD_RANDOM = 'random'
CMD_REG    = 'reg'

CMD_LIST = (
    CMD_HELP,
    CMD_HI,
    CMD_INFO,
    CMD_RANDOM,
    CMD_REG,
)


def get_log(debug):
    import logging
    LOG_TPL = '[%(levelname)s] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
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
API_TOKEN = CONF.get('API_TOKEN')
API_URL = 'https://api.telegram.org/bot{}/'.format(API_TOKEN)
BOT_URL = 'https://t.me/{}'.format(CONF.get('BOT_NAME'))
log = get_log(ARG.debug)


if not os.path.isfile(CONF_FP) or not CONF or 'test' in API_TOKEN:
    write_conf(dict(API_TOKEN='test', BOT_NAME='test_bot'), CONF_FP)
    print(API_TOKEN, API_URL)
    print(f'Please edit {CONF_FN}')
    sys.exit(1)


def write_last_msg(data):
    write_conf(data, LAST_MSG_FN)


def request_url(url):
    from urllib.error import HTTPError, URLError
    from socket import timeout

    try:
        return urllib.request.urlopen(url, timeout=5).read()
    except (HTTPError, URLError) as error:
        log.error('Data is not retrieved. Error: {}\n'.format(error))
    except timeout:
        log.error('Time out\n')
    return ''


def encode_message(text):
    return urllib.parse.quote(text)


def parse_message_cmd(text):
    result = ('', '')
    _regex = re.compile(r'^\/(?P<cmd>\w+)\s+(?P<text>\w+).*$')
    match = _regex.match(text)
    if match:
        result = (match.group('cmd'), match.group('text'))
    return result


def parse_cmd(text):
    result = ''
    _regex = re.compile(r'^\/(?P<cmd>\w+).*$')
    match = _regex.match(text)
    if match:
        result = match.group('cmd')
    return result


def get_cmd_list():
    return ['/{}'.format(x) for x in CMD_LIST]


def get_url(url):
    # response = requests.get(url)
    # content = response.content.decode('utf-8')
    content = request_url(url)
    log.debug(content)
    if content:
        return content.decode('utf-8')
    return content


def get_json_from_url(url):
    data = get_url(url)
    if data:
        return json.loads(data)


def get_updates(offset=None):
    url = API_URL + 'getUpdates'
    if offset:
        url = '{}?offset={}'.format(url, offset)
    json_data = get_json_from_url(url)
    if not json_data:
        return {}
    return json_data


def get_chat_data(raw_msg):
    msg_key = 'message'

    msg_id = None
    text = None
    chat_id = None
    first_name = None
    update_id = raw_msg['update_id']

    if not raw_msg.get(msg_key):
        msg_key = 'edited_message'

    try:
        msg_id = raw_msg[msg_key]['message_id']
        text = raw_msg[msg_key]['text']
        chat_id = raw_msg[msg_key]['chat']['id']
        first_name = raw_msg[msg_key]['chat']['first_name']
    except KeyError:
        pprint(raw_msg)
        log.warning('Key not found')
    return (text, chat_id, first_name, msg_id, update_id, raw_msg)


def send_message(text, chat_id, to_stdout=ARG.to_stdout):
    if to_stdout:
        log.warning('Test mode. Message sent to stdout')
        log.warning(text)
        return
    text = encode_message(text)
    url = API_URL + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
    get_url(url)


def print_start_msg():
    print('\n')
    log.info('You can test this telegram bot via this link 👉 {} 👈'.format(BOT_URL))


def main():
    print_start_msg()

    while True:
        try:
            data = get_updates()['result']
        except Exception as e:
            log.error(e)
            log.error('getUpdates fail')
            data = []

        while data:
            text, chat, first_name, msg_id, update_id, raw_msg = get_chat_data(data.pop(0))

            print_start_msg()
            log.info(f'Message: \"{text}\", chat_id: \"{chat}\", message_id: \"{msg_id}\"')

            cmd, extra_text = parse_message_cmd(text)
            if all((cmd, extra_text)):
                log.warning(f'Command: /{cmd} | text: {extra_text}')
            elif parse_cmd(text):
                cmd = parse_cmd(text)
                log.warning(f'Command: /{cmd}')

            if cmd == CMD_INFO:
                info_list = ('Raspberry Pi', 'Orange Pi', 'Odroid', 'Latte Panda', 'Banana Pi')
                send_message('\n'.join(info_list), chat)
            elif cmd in (CMD_HELLO, CMD_HI):
                send_message(f'Hello, {first_name} 🖖 ', chat)
            elif cmd == CMD_HELP:
                send_message('All commands:\n{}'.format('\n'.join(get_cmd_list())), chat)
            elif cmd == CMD_RANDOM:
                send_message('{}'.format(random.randint(1, 6)), chat)
            else:
                send_message('Unknown command {}. Please try /{}'.format(cmd, CMD_HELP), chat)

            if not data:
                # need to remove messages from telegram server after send
                get_updates(update_id + 1) # looks fine lol

        time.sleep(0.5)


if __name__ == '__main__':
    main()
