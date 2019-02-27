import os
import json

to_list = []


class Mail():
    def __init__(self, to_list, sender, subject='Hello', message='Hello World!'):
        self.to_list = to_list
        self.sender = sender
        self.subject = subject
        self.message = message

    def get_dict(self):
        return dict(to_list=self.to_list, sender=self.sender, subject=self.subject, message=self.message)

    def show_message(self):
        # print(self.get_dict())
        print('From: {to_list} To: {sender}\nSubject: {subject}\nMessage: {message}'.format(**self.get_dict()))


mail = Mail(['user1@gmail.com', 'user2@gmail.com'], 'spamer003@gmail.com')
mail.show_message()
