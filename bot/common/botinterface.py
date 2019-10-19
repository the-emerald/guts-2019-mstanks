import math
from typing import Dict

from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes
from bot.controller.tracker import Tracker


class BotInterface:
    def __init__(self, game_server: ServerComms, name: str, tracker: Tracker):
        self.game_server = game_server
        self.game_server.sendMessage(ServerMessageTypes.CREATETANK, {'Name': name})
        self.name = name
        self.pos = [0, 0]
        self.heading = 0
        self.turret_heading = 0
        self.target = None
        self.tracker = tracker
        self.health = None
        self.ammo = None

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
        if message['messageType'] == ServerMessageTypes.OBJECTUPDATE and message['Name'] == self.name:
            self.pos = self.get_coords(message)
            self.heading = message['Heading']
            self.turret_heading = message['TurretHeading']
            self.health = message['Health']
            self.ammo = message['Ammo']

    def dodge(self, selfpos, selfheading: int, firepos, fireheading: int):
        a = self.angle_to_object(firepos)
        b = (a + 180) % 360
        if b == fireheading:
            heading = None
            if a - 10 <= selfheading <= a + 10:
                heading = (firepos + 90) % 360
            elif b - 10 <= selfheading <= b + 10:
                heading = (firepos - 90) % 360

            if heading:
                self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": heading})
                self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 15})

        return

    def rx(self):
        raise NotImplementedError

    def action(self):
        raise NotImplementedError

    @staticmethod
    def get_coords(payload):
        """
        Helper function that makes a tuple of coordinates from a payload
        :param payload: Dictionary payload
        :return: The tuple of coordinates
        """
        return payload["X"], payload["Y"]
