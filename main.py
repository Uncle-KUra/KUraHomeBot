#!/usr/bin/env python3

import time
import argparse
import json

import telepot
from telepot.loop import MessageLoop

ALLOWED_USERS = 'allowed_users'
TOKEN = 'token'

config = {ALLOWED_USERS: [], TOKEN: None}


class User:
    def __init__(self, user):
        self.sub_modes = list()
        self.current_submode = None
        self.user = user


users = dict()


def get_user_by_chat_id(chat_id):
    if chat_id not in config['allowed_users']:
        return None

    if chat_id not in users:
        users[chat_id] = User(chat_id)

    return users[chat_id]


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    user = get_user_by_chat_id(chat_id)

    if not user:
        bot.sendMessage(chat_id, 'Not allowed to talk with you')
        print('not allowed', chat_id, msg['chat']['first_name'])
    else:
        bot.sendMessage(chat_id, 'ok')


if __name__ == '__main__':
    print('Start...')
    parser = argparse.ArgumentParser(description='KUraBot')
    parser.add_argument('--config', dest='config', help='config file')
    args = parser.parse_args()

    with open(args.config) as config_file:
        config = json.load(config_file)

    print('Config token:', config[TOKEN])
    print('Config allowed users:', config[ALLOWED_USERS])

    bot = telepot.Bot(config[TOKEN])
    MessageLoop(bot, handle).run_as_thread()
    print('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)
