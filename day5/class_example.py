import os
import json
from datetime import datetime


class Mail():
    def __init__(self, to_list, sender, sender_password='password', subject='Hello', message='Hello World!', host='smtp.gmail.com', port=587, debug=True, config_fn='settings.json'):
        self.to_list = to_list
        self.sender = sender
        self.sender_password = sender_password
        self.subject = subject
        self.message = message
        self.host = host
        self.port = port
        self.debug = debug
        self.config_fn = config_fn
        self.data = self.get_dict()

    def __str__(self):
        return 'class Mail()\n{}'.format(json.dumps(self.data))

    def write_conf(self, data, fp):
        with open(fp, 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True)

    def get_dict(self):
        return dict(to_list=' '.join(self.to_list), sender=self.sender, subject=self.subject, message=self.message)

    def show_message(self):
        # print(self.get_dict())
        message = 'From: {sender}\nTo: {to_list}\nSubject: {subject}\nMessage: {message}'.format(**self.get_dict())
        # print(message)
        return message

    def send_message(self):
        if self.debug:
            print(f'Host: {self.host}; Port: {self.port}')
        print(self.show_message())
        print('Email sent!')

    def date2json(self, dt_obj, fmt='%Y-%m-%d %H:%M:%S'):
        return dt_obj.strftime(fmt)

    def save_config(self):
        if self.debug:
            print(f'Data saved to \"{self.config_fn}\"')
        self.data.update(
            dict(
                date_ts=self.date2json(datetime.now())
            )
        )
        self.write_conf(self.data, self.config_fn)
        self.write_conf(dict(host=self.host, port=self.port), 'server.json')


mail = Mail(['user1@gmail.com', 'user2@gmail.com'], debug=True, sender='spamer003@gmail.com')
mail.save_config()
mail.send_message()
