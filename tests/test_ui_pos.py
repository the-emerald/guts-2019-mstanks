from controller.controllerui import *


def test_ui_pos_min():
    x, y = pos_to_canvas((GAME_MIN_X, GAME_MIN_Y))
    assert x == CANVAS_BORDER
    assert y == CANVAS_BORDER


def test_ui_pos_max():
    x, y = pos_to_canvas((-GAME_MIN_X, -GAME_MIN_Y))
    assert x == CANVAS_W + CANVAS_BORDER
    assert y == CANVAS_H + CANVAS_BORDER


def test_ui_pos_area():
    x1, y1 = pos_to_canvas((GAME_MIN_X, GAME_MIN_Y))
    x2, y2 = pos_to_canvas((-GAME_MIN_X, -GAME_MIN_Y))

    w = x2 - x1
    h = y2 - y1
    assert w == CANVAS_W
    assert h == CANVAS_H
