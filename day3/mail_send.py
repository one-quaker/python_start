import json
import time
import os
import sys
import argparse
import smtplib


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
    email_list = [
        'user1@gmail.com',
        'user2@gmail.com',
        'user3@gmail.com',
    ]
    message = dict(
        text='Message body text',
        subject='Message subject here'
    )
    data = dict(
        email_list=email_list,
        message=message,
        user={'from': 'your.email@gmail.com', 'password': 'your_password_here'},
    )
    write_conf(data, CONF_FP)
    print(f'Please edit {CONF_FN}')
    sys.exit(1)


log.info(CONF['message'])


try:
    fromaddr = CONF['user']['from']
    toaddrs = CONF['email_list']
    subj = CONF['message']['subject']
    msg = ('From: {0}\r\nTo: {1}\r\nSubject: {2}\r\n\r\n'.format(
        fromaddr,
        ', '.join(toaddrs),
        subj,
    ))
    msg += 'Error log:\r\n'
    msg += '\r\n'.join(self.read_log_file())
    server = smtplib.SMTP(self.CONFIG_EMAIL_SERVER)
    # server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(self.CONFIG_EMAIL_USER, self.CONFIG_EMAIL_PASS)
except Exception as e:
    log.error('{}'.format(e))
    log.error('Sending email fail. Check your options in config file')
