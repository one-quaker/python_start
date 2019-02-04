import json
import datetime
import os
from pprint import pprint

import scrapy


CATEGORY_CHOICES = (
    'random',
    'best',
    'byrating',
    'abyss',
    'abysstop',
    'abyssbest',
)


BASE_URL = 'https://bash.im/'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
RESULT_FN = 'result_bash.json'


def date2json(d, fmt=DATE_FORMAT):
    if not d:
        return
    return d.strftime(fmt)


class BashSpider(scrapy.Spider):
    name = 'bashim_spider'
    start_urls = ['{}{}'.format(BASE_URL, os.environ.get('category', CATEGORY_CHOICES[1])), ]

    def parse(self, response):
        data = []
        SET_SELECTOR = '.quote'
        ID_SELECTOR = '.actions a.id ::text'
        DATE_SELECTOR = '.actions span.date ::text'
        RATING_SELECTOR = '.actions .rating-o span ::text'
        TEXT_SELECTOR = '.text'

        for i in response.css(SET_SELECTOR):
            try:
                d = dict(
                    uid=i.css(ID_SELECTOR).extract_first(),
                    date=i.css(DATE_SELECTOR).extract_first(),
                    rating=i.css(RATING_SELECTOR).extract_first(),
                    text=i.css(TEXT_SELECTOR).extract_first().replace('<div class="text">', '').replace('</div>', ''),
                )
                data.append(d)
            except Exception as e:
                print(e)

        self.ts = date2json(datetime.datetime.now())
        self.save_data(dict(result=data, ts=self.ts))
        print('Available categories:\n{}'.format('\n'.join(CATEGORY_CHOICES)))

    def save_data(self, data):
        import json
        with open(RESULT_FN, 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
        with open(RESULT_FN, 'r') as f:
            pprint(json.load(f))
