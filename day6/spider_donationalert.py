import json
import datetime
import os
import sys
from pprint import pprint

import scrapy


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = 'https://www.donationalerts.com'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CONF_FP = os.path.join(ROOT_DIR, 'conf.json')
RESULT_FP = os.path.join(ROOT_DIR, 'result.json')


def date2json(d, fmt=DATE_FORMAT):
    if not d:
        return
    return d.strftime(fmt)


def read_conf(fp):
    data = dict()
    try:
        with open(fp, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    return data


def write_conf(data, fp):
    with open(fp, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True)


if any((not os.path.isfile(CONF_FP), not read_conf(CONF_FP))):
    write_conf(dict(TOKEN='token_here', LIMIT=100), CONF_FP)


class WebSpider(scrapy.Spider):
    name = 'spider'
    conf = read_conf(CONF_FP)
    data = list()
    start_urls = ['{url}/widget/lastdonations?alert_type=1,4,6,8,3,2,5&limit={LIMIT}&token={TOKEN}'.format(url=BASE_URL, **conf), ]

    def parse(self, response):
        SET_SELECTOR = 'div.event-container.b-last-events-widget__list.s-last-events-container div.b-last-events-widget__item--inner'
        USER_BASE = '.b-last-events-widget__item--title'
        USER_SELECTOR = f'{USER_BASE} ::text'
        NAME_SELECTOR = f'{USER_BASE} span._name ::text'
        SUM_SELECTOR = f'{USER_BASE} span._sum ::text'

        for i in response.css(SET_SELECTOR):
            try:
                raw_msg = ';'.join([x.strip() for x in i.css(USER_SELECTOR).extract() if x.strip()])
                donation = i.css(SUM_SELECTOR).extract_first()
                d = dict(
                    raw_msg=raw_msg,
                    subscribe=True if ' Twitch!' in raw_msg else False,
                    user_name=i.css(NAME_SELECTOR).extract_first(),
                    donation=dict(),
                )
                if donation:
                    amount, currency = donation.split(' ')
                    d.update(
                        dict(donation={'amount': amount, 'currency': currency})
                    )
                self.data.append(d)
            except Exception as e:
                print(e)
        self.save_data()

    def save_data(self):
        self.ts = date2json(datetime.datetime.now())
        result = dict(result=self.data, ts=self.ts, ts_fmt=DATE_FORMAT)
        write_conf(result, RESULT_FP)
        pprint(read_conf(RESULT_FP))


print(f'Run: scrapy runspider {sys.argv[0]}')
