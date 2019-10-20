import os
import time
import tkinter
import json
from http import HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

from controller.fatcontroller import Controller
from controller.tracker import ObjectState, Alignment

CANVAS_W = 500
CANVAS_H = 400
GAME_MIN_X = -70
GAME_MIN_Y = -100
CANVAS_BORDER = 5


def pos_to_canvas(pos):
    x, y = pos
    return CANVAS_BORDER + (((x - GAME_MIN_X) / 200) * CANVAS_W), CANVAS_BORDER + (((y - GAME_MIN_Y) / 140) * CANVAS_H)


class ControllerUi:
    def __init__(self, controller: Controller):
        self.controller = controller
        pass

    def draw_tracking(self):
        x1, y1 = pos_to_canvas((GAME_MIN_X, GAME_MIN_Y))
        x2, y2 = pos_to_canvas((-GAME_MIN_X, -GAME_MIN_Y))

        text = []
        lines = []
        rects = [
            # border
            [x1, y1, x2 - x1, y2 - y1, 'red', 'blue']
        ]

        to_draw = [state for state in self.controller.tracker.positions.values()]
        for state in to_draw:
            x, y = pos_to_canvas(state.pos)
            colour = "black"
            size = 2
            if state.type == "Tank":
                size = 3
                colour = 'cyan' if state.alignment == Alignment.FRIEND else 'red'
            outline = 'green'
            if state.is_stale():
                outline = 'black'
            rects.append([x - size / 2, y - size / 2, size, size, colour, outline])
            text.append([x, y - 5, state.type + '-' + state.name, 'black'])

        return {
            'rects': rects,
            'lines': lines,
            'text': text,
            'tracked': [{'name': s.name, 'pos': [round(p) for p in s.pos]} for s in
                        self.controller.tracker.positions.values()]
        }

    def start_ui(self):
        """
        Render the UI. Never returns, run this on its own thread
        """
        server = ThreadingHTTPServer(('0.0.0.0', 55555), handler(self))
        server.serve_forever()


def handler(ui: ControllerUi):
    class RequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            directory = os.path.dirname(os.path.realpath(__file__)) + '/web/'
            super().__init__(*args, directory=directory, **kwargs)

        def send_head(self):
            if self.path.endswith('map.json'):
                mapjs = json.dumps(ui.draw_tracking())
                data = mapjs.encode('utf-8')
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-Length", len(data))
                self.send_header("Last-Modified",
                                 self.date_time_string(int(time.time())))
                self.end_headers()
                self.wfile.write(data)
                return None
            return super().send_head()

    return RequestHandler
