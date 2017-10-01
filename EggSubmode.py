
import Response


class EggSubmode:
    def __init__(self):
        self.cost = 100
        self.exist = 100
        self.delta = 10

    @staticmethod
    def get_name():
        return "Eggs"

    def start(self, text):
        text = text.strip()
        if text:
            return self.handle_text(text)
        return Response.SubResponse()

    def handle_text(self, text):
        try:
            text = text.strip()
            if text == 'exit':
                return Response.SubResponse(want_exit=True)
            parts = text.split()
            self.cost = float(parts[0])
            self.exist = float(parts[1])
            self.delta = float(parts[2])
            r1 = 'Real add = {}'.format(self.delta / (100 + self.exist) * 100)
            r2 = 'Cost diff = {}'.format(self.cost - self.cost / (100 + self.exist + self.delta) * (100 + self.exist))
            resp = Response.SubResponse()
            resp.add_text_answer(r1)
            resp.add_text_answer(r2)
            return resp
        except Exception as ex:
            resp = Response.SubResponse()
            resp.add_text_answer(str(ex))
            resp.add_text_answer(str(ex.args))
            return resp
