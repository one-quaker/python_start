import json
import time
import os
import sys
import argparse
import urllib
import urllib.request
from pprint import pprint
# import requests


LAST_MSG_FN = 'last_msg.json'
LAST_MSG_FP = os.path.join(os.getcwd(), LAST_MSG_FN)
CONF_FN = 'conf.json'
CONF_FP = os.path.join(os.getcwd(), CONF_FN)


parser = argparse.ArgumentParser(description='Telegram bot')
parser.add_argument('--debug', action='store_true', default=False)
ARG = parser.parse_args()


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
        return urllib.request.urlopen(url, timeout=3).read()
    except (HTTPError, URLError) as error:
        log.error('Data is not retrieved. Error: {}\n'.format(error))
    except timeout:
        log.error('Time out\n')
    return None


def encode_message(text):
    return urllib.parse.quote(text)


def get_url(url):
    # response = requests.get(url)
    # content = response.content.decode('utf8')
    content = request_url(url).decode('utf8')
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = API_URL + 'getUpdates'
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    result_key = 'result'
    if not updates[result_key]:
        print(updates)
        return ()
    num_updates = len(updates[result_key])
    last_update = num_updates - 1
    msg_key = 'message'

    msg_id = None
    text = None
    chat_id = None
    first_name = None
    raw_msg = dict()

    if not updates[result_key][last_update].get(msg_key):
        msg_key = 'edited_message'

    try:
        msg_id = updates[result_key][last_update][msg_key]['message_id']
        text = updates[result_key][last_update][msg_key]['text']
        chat_id = updates[result_key][last_update][msg_key]['chat']['id']
        first_name = updates[result_key][last_update][msg_key]['chat']['first_name']
        raw_msg = updates[result_key][last_update][msg_key]
    except KeyError:
        pprint(updates[result_key][last_update])
        pprint(raw_msg)
        log.warning('Key not found')
    return (text, chat_id, first_name, msg_id, raw_msg)


def send_message(text, chat_id):
    url = API_URL + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
    get_url(url)


def main():
    last_textchat = (None, None)

    while True:
        text, chat, first_name, msg_id, raw_msg = get_last_chat_id_and_text(get_updates())

        LAST_MSG_DB = read_conf(LAST_MSG_FP)
        last_data = dict(text=text, chat=chat, first_name=first_name, msg_id=msg_id)
        last_key = f'message_id_{msg_id}'
        last_msg = {last_key: last_data}

        if not LAST_MSG_DB:
            write_last_msg(last_msg)
        elif last_key not in LAST_MSG_DB.keys():
            LAST_MSG_DB[last_key] = last_msg
            write_last_msg(LAST_MSG_DB)

        if (text, chat) != last_textchat:
            send_message(encode_message(f'Your message \"{text}\" accepted 👍'), chat)
            last_textchat = (text, chat)
            log.info('You can test this telegram bot via this link 👉 {} 👈'.format(BOT_URL))
            log.info(f'Last message: \"{text}\", chat_id: \"{chat}\", message_id: \"{msg_id}\"')
        time.sleep(1)


if __name__ == '__main__':
    main()
