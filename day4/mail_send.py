import json
import time
import os
import sys
import argparse
import smtplib
import threading
from pprint import pprint


CONF_FN = 'conf.json'
CONF_FP = os.path.join(os.getcwd(), CONF_FN)


parser = argparse.ArgumentParser(description='Email send')
parser.add_argument('-D', '--debug', action='store_true', default=False)
parser.add_argument('-f', '--force', action='store_true', default=False)
ARG = parser.parse_args()


def get_log(debug):
    import logging
    LOG_TPL = '[%(levelname)s] %(message)s'
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
log = get_log(ARG.debug)


if any((not os.path.isfile(CONF_FP), not CONF, ARG.force)):
    email_list = (
        'user1@gmail.com',
        'user2@gmail.com',
        'user3@gmail.com',
    )
    message_list = (
        dict(
            subject='Subject1',
            text='Message1 text',
        ),
        dict(
            subject='Subject2',
            text='Message2 text',
        ),
        dict(
            subject='Subject3',
            text='Message3 text',
        ),
    )
    data = dict(
        email_list=email_list,
        message_list=message_list,
        user={'from': 'your.email@gmail.com', 'password': 'your_password_here'},
    )
    write_conf(data, CONF_FP)
    print(f'Please edit {CONF_FN}')
    sys.exit(1)


# log.info(CONF['message_list'])


def send_mail(subj, text, to_email):
    log.debug('\nSubject: {}\nText: {}\n'.format(subj, text))
    try:
        fromaddr = CONF['user']['from']
        msg = 'From: {0}\r\nTo: {1}\r\nSubject: {2}\r\n\r\n'.format(
            fromaddr,
            to_email,
            subj,
        )
        msg += '{}\r\n'.format(text)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(CONF['user']['from'], CONF['user']['password'])
        server.sendmail(fromaddr, to_email, msg)
        server.quit()
        log.info('Email sent!')
    except Exception as e:
        log.error('{}'.format(e))
        log.error('Sending email fail. Check your options in config file')


def mail_send_loop():
    for email in CONF['email_list']:
        for message in CONF['message_list']:
            time.sleep(1)
            send_mail(message['subject'], message['text'], email)


Q = ['Email task #{} done!'.format(x) for x in range(30)]


def t1_test():
    worker_name = 'Worker #1'
    while Q:
        try:
            log.info('{}: \"{}\"'.format(worker_name, Q.pop(0)))
            time.sleep(1)
        except IndexError:
            log.warning('{}: Q is empty'.format(worker_name))


def t2_test():
    worker_name = 'Worker #2'
    while Q:
        try:
            log.info('{}: \"{}\"'.format(worker_name, Q.pop(0)))
            time.sleep(5)
        except IndexError:
            log.warning('{}: Q is empty'.format(worker_name))


t1 = threading.Thread(target=t1_test)
# t1.daemon = True
t1.start()

t2 = threading.Thread(target=t2_test)
# t2.daemon = True
t2.start()
