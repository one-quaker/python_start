import os
import sys
import json
from datetime import datetime
from pprint import pprint


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

import django
from django.db.utils import IntegrityError
django.setup()


from web.models import TwitchUser, TwitchAction, Donation


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


for i in DATA.get('result', []):
    name = i.get('user_name')
    donation = i.get('donation', {})
    subscriber = i.get('subscriber')
    alert_type = i.get('alert_type')
    alert_ts = i.get('alert_ts')
    alert_id = int(i.get('alert_id'))

    try:
        print('\nuser')
        db_user = TwitchUser()
        db_user.name = name
        db_user.save()
    except IntegrityError:
        print(f'\"{name}\", skip...')


    print('\naction')
    _user = TwitchUser.objects.filter(name=name)
    try:
        db_action = TwitchAction()
        db_action.alert_id = alert_id
        db_action.alert_type = int(alert_type)
        db_action.alert_ts = datetime.strptime(alert_ts, DATE_FORMAT)

        if alert_type == '6':
            db_action.subscribe = True
        else:
            db_action.subscribe = False

        if _user:
            db_action.user = _user[0]
        db_action.save()
    except IntegrityError:
        print(f'\"{name}\", skip...')

    if alert_type == '1':
        try:
            print('\ndonation')
            db_donation = Donation()
            db_donation.amount = donation['amount'].replace(',', '.')
            db_donation.currency = donation['currency']
            db_donation.message = donation['message']
            db_donation.alert_id = alert_id
            db_donation.alert_ts = datetime.strptime(alert_ts, DATE_FORMAT)
            db_donation.save()
        except IntegrityError:
            print('\"{name} {amount} {message}\", skip...'.format(name=name, **donation))


    _action = TwitchAction.objects.filter(alert_id=alert_id)
    _donation = Donation.objects.filter(alert_id=alert_id)
    if _action and _donation:
        _db_action = _action[0]
        _db_action.donation = _donation[0]
        _db_action.save()
