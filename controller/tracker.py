import logging
import time
from enum import Enum
from typing import Dict

from common.servermessagetypes import ServerMessageTypes


class Alignment(Enum):
    NEUTRAL = 0
    FRIEND = 1
    FOE = 2


class ObjectState:
    alignment: Alignment
    name: str
    STALE_TIME = 5

    def __init__(self, pos, heading, turret_heading, type, id, name, alignment, last, health, ammo):
        self.health = health
        self.ammo = ammo
        self.priority = False
        self.pos = pos
        self.heading = heading
        self.turret_heading = turret_heading
        self.type = type
        self.id = id
        self.name = name
        self.time = time.time()
        self.alignment = alignment
        self.velocity = (0, 0)
        if last:
            self.priority = last.priority
            x, y = pos
            ox, oy = last.pos
            dx, dy = x - ox, y - oy
            dt = self.time - last.time
            if dt > 0.1:
                self.velocity = (dx / dt, dy / dt)
            else:
                self.velocity = last.velocity

    def is_stale(self):
        return (time.time() - self.time) > ObjectState.STALE_TIME


class Tracker:
    positions: Dict[str, ObjectState]

    def __init__(self, team):
        self.positions = {}
        self.time = 0
        self.team = team + ':'

    def handle_message(self, message, bots):
        if message['messageType'] == ServerMessageTypes.GAMETIMEUPDATE:
            self.time = message['Time']
        if message['messageType'] == ServerMessageTypes.OBJECTUPDATE:
            pos = message['X'], message['Y']
            heading = message['Heading']
            turret_heading = message['TurretHeading']
            name = message['Name']
            id = message['Id']
            type = message['Type']
            alignment = Alignment.NEUTRAL
            health = None
            ammo = None
            if type == 'Tank':
                alignment = Alignment.FRIEND if name.startswith(self.team) else Alignment.FOE
                health = message['Health']
                ammo = message['Ammo']
            last = None
            try:
                last = self.positions[id]
            except KeyError:
                pass
            state = ObjectState(pos, heading, turret_heading, type, id, name, alignment, last, health, ammo)
            for bot in bots:
                if bot.name == state.name:
                    bot.ammo = state.ammo
                    bot.health = state.health
            self.positions[id] = state
            logging.debug('Tracked %s at %s', name, pos)
        if message['messageType'] == ServerMessageTypes.SNITCHPICKUP:
            self.positions[message['Id']].priority = True

    def shoot_at(self, bot: ObjectState):
        if bot.is_stale():
            return False
        if bot.type != 'Tank':
            return False
        if bot.alignment == Alignment.FOE:
            return True
        if bot.alignment == Alignment.FRIEND and bot.health == 1:
            return True
        return False

    def closest_enemy(self, bot):
        closest = 9999
        closest_state = None

        for v in self.positions.values():
            if v.name != bot.name and self.shoot_at(v):
                if v.priority:
                    return v
                dist = bot.distance_to_object(v.pos)
                if dist < closest:
                    closest = dist
                    closest_state = v

        return closest_state

    def closest_pickup(self, bot):
        closest = 9999
        closest_state = None

        for v in self.positions.values():
            if v.type.endswith('Pickup') and not v.is_stale():
                dist = bot.distance_to_object(v.pos)
                if dist < closest:
                    closest = dist
                    closest_state = v

        return closest_state
