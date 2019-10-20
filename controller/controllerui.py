import time
import tkinter

from controller.fatcontroller import Controller
from controller.tracker import ObjectState, Alignment

CANVAS_W = 200
CANVAS_H = 200
CANVAS_BORDER = 5


def pos_to_canvas(pos):
    x, y = pos
    return CANVAS_BORDER + (((x + 100) / 200) * CANVAS_W), CANVAS_BORDER + (((y + 70) / 140) * CANVAS_H)


class ControllerUi:
    def __init__(self, controller: Controller):
        self.controller = controller
        pass

    def draw_tracking(self, c: tkinter.Canvas):
        c.delete("all")

        x1, y1 = pos_to_canvas((-70, -100))
        x2, y2 = pos_to_canvas((70, 100))
        c.create_rectangle(x1, y1, x2, y2, outline='blue')

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
            c.create_rectangle(x - size, y - size, x + size, y + size, fill=colour, outline=outline)

    def start_ui(self):
        """
        Render the UI. Never returns, run this on its own thread
        """
        tk = tkinter.Tk()
        c = tkinter.Canvas(tk, width=CANVAS_W + CANVAS_BORDER*2, height=CANVAS_H + CANVAS_BORDER*2)
        c.pack()

        while True:
            self.draw_tracking(c)
            tk.update_idletasks()
            tk.update()
            time.sleep(0.1)
