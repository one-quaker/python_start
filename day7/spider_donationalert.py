import json
import datetime
import os
import sys
import random
from pprint import pprint

import scrapy
from scrapy.crawler import CrawlerProcess


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = 'https://www.donationalerts.com'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CONF_FP = os.path.join(ROOT_DIR, 'conf.json')
RESULT_FP = os.path.join(ROOT_DIR, 'result.json')
TOKEN_KEY = 'TOKEN'


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
    data = dict(
        LIMIT=100,
        USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0',
    )
    data.update({TOKEN_KEY: 'token_here', })
    write_conf(data, CONF_FP)


CONF = read_conf(CONF_FP)
if 'token' in CONF.get(TOKEN_KEY):
    print(f'Default value found\nPlease edit \"{TOKEN_KEY}\" in {CONF_FP}')
    sys.exit(1)


class WebSpider(scrapy.Spider):
    name = 'spider'
    conf = CONF
    download_delay = random.randint(15, 60) / 10
    data = list()
    url_tpl = '{url}/widget/lastdonations?alert_type={alert_type}&limit={LIMIT}&token={TOKEN}'
    alert_key_list = ('donator', 'subscriber')
    alert_key_idx = 0
    alert_donator = '1'
    alert_subscriber = '4,6,8,3,2,5'
    start_urls = (
        url_tpl.format(url=BASE_URL, alert_type=alert_donator, **conf),
        url_tpl.format(url=BASE_URL, alert_type=alert_subscriber, **conf),
    )
    print(64 * '-', download_delay)

    def extract_strip(self, data):
        return ';'.join([x.strip() for x in data if x.strip()])

    def parse(self, response):
        SET_SELECTOR = 'div.scroll-container div.event-container div.event'
        USER_BASE = 'div.b-last-events-widget__item--inner .b-last-events-widget__item--title'
        USER_SELECTOR = f'{USER_BASE} ::text'
        NAME_SELECTOR = f'{USER_BASE} span._name ::text'
        SUM_SELECTOR = f'{USER_BASE} span._sum ::text'
        MSG_SELECTOR = 'div.message-container ::text'

        DATA_KEY = self.alert_key_list[self.alert_key_idx]

        for i in response.css(SET_SELECTOR):
            try:
                raw_msg = self.extract_strip(i.css(USER_SELECTOR).extract())
                donation = i.css(SUM_SELECTOR).extract_first()
                d = dict(
                    alert_id=i.attrib.get('data-alert_id'),
                    alert_type=i.attrib.get('data-alert_type'),
                    alert_ts=i.css('input#date_created').attrib['value'],
                    raw_msg=raw_msg,
                    user_name=i.css(NAME_SELECTOR).extract_first(),
                    donation=dict(),
                )
                d.update(
                    {DATA_KEY: True}
                )
                if donation:
                    amount, currency = donation.split(' ')
                    message = self.extract_strip(i.css(MSG_SELECTOR).extract())
                    d.update(
                        dict(donation={
                            'amount': amount, 'currency': currency,
                            'message': message,
                        })
                    )
                self.data.append(d)
            except Exception as e:
                print(e)
        self.alert_key_idx += 1
        if DATA_KEY == self.alert_key_list[-1]:
            self.save_data()

    def save_data(self):
        self.ts = date2json(datetime.datetime.now())
        result = dict(result=self.data, ts=self.ts, ts_fmt=DATE_FORMAT)
        write_conf(result, RESULT_FP)
        pprint(read_conf(RESULT_FP))


process = CrawlerProcess({
    'USER_AGENT': CONF.get('USER_AGENT'),
})

process.crawl(WebSpider)
process.start() # the script will block here until the crawling is finished
