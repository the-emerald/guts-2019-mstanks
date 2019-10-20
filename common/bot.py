import logging
import math
import time
from typing import Dict

from common.servercomms import ServerComms
from common.servermessagetypes import ServerMessageTypes
from controller.tracker import Tracker


class Bot:
    heading: int

    def __init__(self, game_server: ServerComms, name: str, tracker: Tracker):
        self.last_fire_time = 0
        self.game_server = game_server
        self.game_server.sendMessage(ServerMessageTypes.CREATETANK, {'Name': name})
        self.name = name
        self.pos = [0, 0]
        self.ammo = 4
        self.kills = 0
        self.heading = 0
        self.turret_heading = 0
        self.health = 3
        self.target = None
        self.tracker = tracker
        self.movement_strategy = None
        self.turret_strategy = None
        self.last_message = None
        self.respawn_time = None
        logging.info("Spawned bot %s", name)

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message)  # Does the updating
        return self.last_message

    def distance_to_object(self, coordinate: tuple):
        ox, oy = self.pos
        x, y = coordinate
        delta_x = x - ox
        delta_y = y - oy
        return math.sqrt(delta_x ** 2 + delta_y ** 2)

    def angle_to_object(self, coordinate: tuple):
        ox, oy = self.pos
        x, y = coordinate
        delta_x = x - ox
        delta_y = y - oy
        return abs(((math.atan2(delta_y, delta_x) * (180 / math.pi)) - 360)) % 360

    def handle_message(self, message: Dict):
        ty = message['messageType']
        if ty == ServerMessageTypes.OBJECTUPDATE and message['Name'] == self.name:
            self.pos = self.get_coords(message)
            self.heading = message['Heading']
            self.turret_heading = message['TurretHeading']
        if ty == ServerMessageTypes.KILL:
            self.kills += 1
            logging.info("%s scored a point", self.name)
        if ty == ServerMessageTypes.AMMOPICKUP:
            self.ammo = 10
        if ty == ServerMessageTypes.HITDETECTED:
            logging.info("%s hit", self.name)
            self.health -= 1
        if ty == ServerMessageTypes.DESTROYED:
            logging.info("Died bot %s", self.name)
            self.respawn_time = time.time() + 5
        return

    def on_respawn(self):
        self.respawn_time = None
        self.health = 3
        self.ammo = 10

    def need_dodge(self, firepos, fireheading):
        a = self.angle_to_object(firepos)
        b = (a + 180) % 360
        if b == fireheading:
            self.dodge(firepos, a, b)

    def dodge(self, firepos, a, b):
        heading = None
        if ((a - 10) % 360) <= self.heading <= ((a + 10) % 360):
            heading = (firepos + 90) % 360
        elif ((b - 10) % 360) <= self.heading <= ((b + 10) % 360):
            heading = (firepos - 90) % 360
        if heading:
            self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": heading})
            self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 15})

    def return_to_goal(self):
        def get_close():
            self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": self.angle_to_object(goal)})
            self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})
            time.sleep(1)

        x, y = self.pos
        at_goal = 0
        if y >= 0:
            goal = 0, 101
            while not at_goal:
                x, y = self.pos
                if y >= 90:
                    while abs(x) >= 15:
                        goal = 0, 89
                        get_close()
                        goal = 0, 101
                    get_close()
                get_close()
                if self.compare_pos(goal):
                    at_goal = 1
        else:
            goal = 0, -101
            while not at_goal:
                x, y = self.pos
                if y <= -90:
                    while abs(x) >= 15:
                        goal = 0, -89
                        get_close()
                        goal = 0, -101
                    get_close()
                get_close()
                if self.compare_pos(goal):
                    at_goal = 1

    def compare_pos(self, loc):
        return self.distance_to_object(loc) < 10

    def action(self):
        if self.movement_strategy:
            self.movement_strategy.action(self)

    @staticmethod
    def get_coords(payload):
        """
        Helper function that makes a tuple of coordinates from a payload
        :param payload: Dictionary payload
        :return: The tuple of coordinates
        """
        return payload["X"], payload["Y"]

    def can_fire(self):
        # TODO: ammo state?
        return self.ammo > 0 and (time.time() - self.last_fire_time) > 2

    def fire(self):
        if self.can_fire():
            self.ammo -= 1
            self.last_fire_time = time.time()
            self.game_server.sendMessage(ServerMessageTypes.FIRE)
        else:
            logging.warning("can't fire for %s as recently fired", self.name)
        pass

    def turn_turret_to_heading(self, heading):
        self.game_server.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {"Amount": heading})
