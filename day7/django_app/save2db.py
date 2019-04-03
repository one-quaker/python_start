import os
import sys
import json
from datetime import datetime
from pprint import pprint
import argparse


# TODO: add agrparse


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

import django
from django.db.utils import IntegrityError
django.setup()


from web.models import Post, Author


def read_conf(fp):
    data = dict()
    try:
        with open(fp, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    return data


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATA = read_conf(sys.argv[1])
# pprint(DATA)


for post in DATA['result']:
    author_obj, created = Author.objects.get_or_create(
        nickname=post['author'],
    )

    post.pop('author')

    try:
        p = Post(
            author=author_obj,
            **post,
        )
        p.save()
    except IntegrityError:
        print('Post already in database, skip...')
