import os
import sys
import json
from datetime import datetime
from pprint import pprint


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

import django
from django.db.utils import IntegrityError
django.setup()


from web.models import TwitchUser, Subscribe, Donation, DonationAlertEvent


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


def clear_db():
    # TwitchUser.objects.all().delete()
    DonationAlertEvent.objects.all().delete()
    # Donation.objects.all().delete()
    Donation.objects.filter(source=Donation.DALERT).delete()
    Subscribe.objects.all().delete()


def load_data():
    for i in DATA.get('result', []):
        name = i.get('user_name')
        donation = i.get('donation', {})
        subscriber = i.get('subscriber')
        alert_type = i.get('alert_type')
        alert_ts = i.get('alert_ts')
        alert_id = int(i.get('alert_id'))

        try:
            print('\ndonation raw')
            db_devent = DonationAlertEvent()
            db_devent.alert_id = alert_id
            db_devent.alert_ts = datetime.strptime(alert_ts, DATE_FORMAT)
            db_devent.raw_data = i
            db_devent.save()
        except IntegrityError:
            print(f'\"{name}\", skip...')

        try:
            print('\nuser')
            db_user = TwitchUser()
            db_user.name = name
            db_user.save()
        except IntegrityError:
            print(f'\"{name}\", skip...')

        _user = TwitchUser.objects.filter(name=name)
        if alert_type == '6':
            print('\nsubscribe')
            try:
                db_sub = Subscribe()
                db_sub.alert_ts = datetime.strptime(alert_ts, DATE_FORMAT)
                db_sub.user = _user[0]
                db_sub.save()
            except IntegrityError:
                print(f'\"{name}\", skip...')

        _donation = Donation.objects.filter(alert_id=alert_id)
        if alert_type == '1' and not _donation:
            try:
                print('\ndonation')
                db_donation = Donation()
                db_donation.amount = donation['amount'].replace(',', '.')
                db_donation.currency = donation['currency']
                db_donation.message = donation['message']
                db_donation.source = Donation.DALERT
                if _user:
                    db_donation.user = _user[0]
                db_donation.alert_id = alert_id
                db_donation.alert_ts = datetime.strptime(alert_ts, DATE_FORMAT)
                db_donation.save()
            except IntegrityError:
                print('\"{name} {amount} {message}\", skip...'.format(name=name, **donation))


# clear_db()
load_data()
