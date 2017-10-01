#!/usr/bin/env python3

import time
import argparse
import json

import telepot
from telepot.loop import MessageLoop

import Response

import EggSubmode


ALLOWED_USERS = 'allowed_users'
TOKEN = 'token'
DEBUG = 'debug'

TEXT = 'text'

config = {ALLOWED_USERS: [], TOKEN: None, DEBUG: False}


class User:
    def __init__(self, user):
        self.sub_modes = dict()
        self.register(EggSubmode.EggSubmode())
        self.current_submode = None
        self.user = user
        self.submode_state = dict()

    def register(self, submode):
        self.sub_modes[submode.get_name()] = submode
        self.sub_modes[submode.get_name().lower()] = submode

    def convert_response(self, resp, sub_response):
        for ans in sub_response.answers:
            if ans.type == Response.ANSWER_TEXT:
                resp.add_text_answer(self.user, ans.text)

    def set_submode_state(self, submode, state):
        self.submode_state[submode.get_name()] = state

    def get_submode_state(self, submode):
        return self.submode_state.get(submode.get_name(), None)

    @staticmethod
    def print_input_debug(msg):
        if not config[DEBUG]:
            return
        content_type, chat_type, chat_id = telepot.glance(msg)
        text = 'NOT A TEXT'
        if content_type == TEXT:
            text = msg[TEXT]
        print(content_type, chat_type, chat_id, text, sep=' || ')

    @staticmethod
    def print_output_debug(debug):
        if not config[DEBUG]:
            return
        for x in debug:
            print('DEBUG:', x)

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.print_input_debug(msg)
        status = Response.STATUS_OK
        resp = Response.Response()
        sub_resp = None
        if content_type == TEXT:
            text_parts = msg[TEXT].strip().split(' ', 1) + ['']
            if self.current_submode is None:
                if text_parts[0] in self.sub_modes:
                    self.current_submode = self.sub_modes[text_parts[0]]
                    state = self.get_submode_state(self.current_submode)
                    sub_resp = self.current_submode.start(text_parts[1], state)
                    self.convert_response(resp, sub_resp)
            else:
                state = self.get_submode_state(self.current_submode)
                sub_resp = self.current_submode.handle_text(msg[TEXT].strip(), state)
                self.convert_response(resp, sub_resp)
        if sub_resp:
            if self.current_submode and sub_resp.state:
                self.set_submode_state(self.current_submode, sub_resp.state)
            if sub_resp.want_exit:
                self.current_submode = None
            self.print_output_debug(sub_resp.debug)

        resp.status = status
        return resp


users = dict()


def get_user_by_chat_id(chat_id):
    if chat_id not in config[ALLOWED_USERS]:
        return None

    if chat_id not in users:
        users[chat_id] = User(chat_id)

    return users[chat_id]


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    user = get_user_by_chat_id(chat_id)

    if not user:
        bot.sendMessage(chat_id, 'Not allowed to talk with you')
        print('not allowed', chat_id, msg['chat']['first_name'])
    else:
        resp = user.handle(msg)
        if resp.status == Response.STATUS_OK:
            for answer in resp.answers:
                if answer.type == Response.ANSWER_TEXT:
                    bot.sendMessage(answer.chat_id, answer.text)


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
