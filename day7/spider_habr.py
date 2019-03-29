import json
import datetime
import os
import sys
import random
import argparse
from pprint import pprint

import scrapy
from scrapy.crawler import CrawlerProcess


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = 'https://habr.com/{}/'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CONF_FP = os.path.join(ROOT_DIR, 'conf_habr.json')
RESULT_FP = os.path.join(ROOT_DIR, 'result_habr.json')
SAVE2DB_FP = os.path.join(ROOT_DIR, 'django_app', 'save2db.py')


parser = argparse.ArgumentParser()
parser.add_argument('-S', '--skip-db', action='store_true', default=False)
parser.add_argument('-G', '--get-images', action='store_true', default=False)
parser.add_argument('-U', '--update', action='store_true', default=False)
parser.add_argument('-D', '--debug', action='store_true', default=False)


ARG = parser.parse_args()


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
    write_conf(data, CONF_FP)


IMG_ROOT = os.path.join(ROOT_DIR, 'img')
if not os.path.isdir(IMG_ROOT):
    os.mkdir(IMG_ROOT)


CONF = read_conf(CONF_FP)


class WebSpider(scrapy.Spider):
    name = 'spider'
    conf = CONF
    download_delay = random.randint(15, 60) / 10
    data = list()
    start_urls = (
        BASE_URL.format('ru'),
        # BASE_URL.format('en'),
    )
    print(64 * '-', download_delay)

    def parse(self, response):
        SET_SELECTOR = 'div.posts_list ul.content-list article.post'
        TITLE_SELECTOR = 'h2.post__title a ::text'
        POST_BASE = 'div.post__body'
        URL_SELECTOR = f'{POST_BASE} a.post__habracut-btn'
        IMG_SELECTOR = f'{POST_BASE} div.post__text img'
        TEXT_SELECTOR = f'{POST_BASE} div.post__text'

        POST_FOOTER_BASE = 'footer.post__footer li'
        RATING_SELECTOR = f'{POST_FOOTER_BASE} span.js-score ::text'
        BOOKMARK_SELECTOR = f'{POST_FOOTER_BASE} span.bookmark__counter ::text'
        COMMENT_SELECTOR = f'{POST_FOOTER_BASE} span.post-stats__comments-count ::text'
        VIEW_SELECTOR = f'{POST_FOOTER_BASE} span.post-stats__views-count ::text'

        TAG_SELECTOR = 'ul.post__hubs'

        for i in response.css(SET_SELECTOR):
            title = i.css(TITLE_SELECTOR).extract_first()
            url = i.css(URL_SELECTOR).attrib['href']
            img = i.css(IMG_SELECTOR).attrib.get('src', '')
            text = i.css(TEXT_SELECTOR).extract_first()
            rating = int(i.css(RATING_SELECTOR).extract_first())
            bookmark = int(i.css(BOOKMARK_SELECTOR).extract_first())

            try:
                comment = int(i.css(COMMENT_SELECTOR).extract_first())
            except:
                print('Wrong comment count')
                comment = 0

            raw_view = i.css(VIEW_SELECTOR).extract_first()
            view = int(float(raw_view.replace('k', '').replace(',', '.')) * 1000)
            tag_list = i.css('ul.post__hubs li.inline-list__item a.inline-list__item-link ::text').extract()

            try:
                d = dict(
                    title=title,
                    url=url,
                    cover=img,
                    text=text,
                    rating=rating,
                    bookmark=bookmark,
                    comment=comment,
                    view=view,
                    tag_list=tag_list,
                )
                self.data.append(d)
            except Exception as e:
                print(e)

            if img and ARG.get_images:
                out = os.popen(f'wget -c {img} -P {IMG_ROOT}').read()
                print(out)
        self.save_data()

    def save_data(self):
        self.ts = date2json(datetime.datetime.now())
        result = dict(result=self.data, ts=self.ts, ts_fmt=DATE_FORMAT)
        write_conf(result, RESULT_FP)
        pprint(read_conf(RESULT_FP))


process = CrawlerProcess({
    'USER_AGENT': CONF.get('USER_AGENT'),
})


if ARG.update:
    process.crawl(WebSpider)
    process.start() # the script will block here until the crawling is finished


if not ARG.skip_db:
    cmd = '{} {} {}'.format(sys.executable, SAVE2DB_FP, RESULT_FP)
    print(cmd)
    out = os.popen(cmd).read()
    print(out)
