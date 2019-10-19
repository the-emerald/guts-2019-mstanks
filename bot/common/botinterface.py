import math

from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes


class BotInterface:
    def __init__(self, game_server: ServerComms, name: str):
        self.game_server = game_server
        self.game_server.sendMessage(ServerMessageTypes.CREATETANK, {'Name': name})
        # TODO: set xpos and ypos

    @staticmethod
    def get_coords(payload):
        """
        Helper function that makes a tuple of coordinates from a payload
        :param payload: Dictionary payload
        :return: The tuple of coordinates
        """
        return payload["X"], payload["Y"]

    def angle_to_object(self, coordinate: tuple):
        x, y = coordinate
        delta_x = self.xpos - x
        delta_y = self.ypos - y
        return math.sqrt(delta_x ** 2 + delta_y ** 2)

    def distance_to_object(self, coordinate: tuple):
        x, y = coordinate
        delta_x = self.xpos - x
        delta_y = self.ypos - y
        return ((math.atan2(delta_y, delta_x)*(180/math.pi)) - 360) % 360

    def rx(self):
        raise NotImplementedError

    def action(self):
        raise NotImplementedError

