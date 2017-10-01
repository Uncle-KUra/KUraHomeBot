
import Response

COST = 'cost'


class EggSubmode:
    def __init__(self):
        pass

    @staticmethod
    def get_name():
        return "Eggs"

    def start(self, text, state):
        text = text.strip()
        if text:
            return self.handle_text(text, state)
        return Response.SubResponse()

    @staticmethod
    def calculate(cost, exist, delta):
        r1 = 'Real add = {}'.format(delta / (100 + exist) * 100)
        r2 = 'Cost diff = {}'.format(cost - cost / (100 + exist + delta) * (100 + exist))
        return r1, r2

    def handle_text(self, text, state):
        if not state:
            state = dict()
        try:
            text = text.strip().lower()
            if text == 'exit':
                return Response.SubResponse(want_exit=True)
            parts = text.split()
            resp = Response.SubResponse()
            if len(parts) == 3:
                cost = float(parts[0])
                old = float(parts[1])
                add = float(parts[2])
            elif len(parts) == 2 and COST in state:
                cost = state[COST]
                old = float(parts[0])
                add = float(parts[1])
            else:
                resp.add_text_answer("Format: [cost] exist delta")
                return resp
            r1, r2 = self.calculate(cost, old, add)
            resp.add_text_answer(r1)
            resp.add_text_answer(r2)
            resp.store_state({COST: cost})
            return resp
        except Exception as ex:
            resp = Response.SubResponse()
            resp.add_text_answer('uuups')
            resp.add_text_answer(str(ex))
            resp.add_text_answer(str(ex.args))
            return resp
