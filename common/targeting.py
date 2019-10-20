import math
from math import sqrt

from controller.tracker import ObjectState, Alignment

round_speed = 10


def calculate_firing_solution(gun_position: tuple, target: ObjectState) -> float:
    # https://stackoverflow.com/questions/2248876/2d-game-fire-at-a-moving-target-by-predicting-intersection-of-projectile-and-u

    xg, yg = gun_position
    xt, yt = target.pos
    vtx, vty = target.velocity # Will be implemented later

    a = vtx**2 + vty**2 - round_speed**2
    b = 2 * (vtx * (xt - xg) + vty * (yt - yg))
    c = (xt - xg)**2 + (yt - yg)**2

    disc = b**2 - 4*a*c
    if not disc:
        return None

    t1 = (-b + sqrt(disc)) / (2 * a)
    t2 = (-b - sqrt(disc)) / (2 * a)

    t = max(t1, t2)

    ax = t * vtx + xt
    ay = t * vty + yt

    if sqrt(ax**2 + ay**2) >= 100:
        return None

    return abs(((math.atan2(ay - yg, ax - xg) * (180 / math.pi)) - 360)) % 360


def check_firing_solution_clear(targets: dict, gun_position: tuple, solution: float):
    for key, value in targets.items():
        if value.alignment != Alignment.FRIEND:
            continue
        if abs(solution-calculate_firing_solution(gun_position, value)) <= 5:
            return True
    return False
