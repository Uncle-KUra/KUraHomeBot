#!/usr/bin/env python3

STATUS_OK = 'OK'

ANSWER_TEXT = 'TEXT'


class Answer:
    def __init__(self, chat_id):
        self.chat_id = chat_id


class TextAnswer(Answer):
    def __init__(self, chat_id, text):
        super().__init__(chat_id)
        self.text = text
        self.type = ANSWER_TEXT


class Response:
    def __init__(self, status=STATUS_OK):
        self.answers = list()
        self.status = status

    def add_text_answer(self, chat_id, text):
        self.answers.append(TextAnswer(chat_id, text))


class SubTextAnswer:
    def __init__(self, text):
        self.text = text
        self.type = ANSWER_TEXT


class SubResponse:
    def __init__(self, status=STATUS_OK, want_exit=False):
        self.answers = list()
        self.status = status
        self.want_exit = want_exit
        self.state = None

    def add_text_answer(self, text):
        self.answers.append(SubTextAnswer(text))

    def store_state(self, data):
        self.state = data
