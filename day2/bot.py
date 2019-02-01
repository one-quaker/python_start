import json
import time
import os
from pprint import pprint
import requests


CONF_FN = 'conf.json'
CONF_FP = os.path.join(os.getcwd(), CONF_FN)


def write_conf(data, fp=CONF_FP):
    with open(fp, 'w') as f:
        json.dump(data, f)


def read_conf(fp=CONF_FP):
    data = dict()
    with open(fp, 'r') as f:
        data = json.load(f)
    return data


TOKEN = read_conf().get('TOKEN')
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

if 'test' in TOKEN:
    print(TOKEN, URL)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode('utf8')
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + 'getUpdates'
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates['result'])
    last_update = num_updates - 1
    text = updates['result'][last_update]['message']['text']
    chat_id = updates['result'][last_update]['message']['chat']['id']
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
    get_url(url)


# text, chat = get_last_chat_id_and_text(get_updates())
# send_message(text, chat)


def main():
    last_textchat = (None, None)
    while True:
        text, chat = get_last_chat_id_and_text(get_updates())
        # if (text, chat) != last_textchat:
        #     send_message(text, chat)
        #     last_textchat = (text, chat)
        pprint(text, chat)
        time.sleep(3)


if __name__ == '__main__':
    main()
