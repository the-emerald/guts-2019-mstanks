from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes


class BotInterface:
    def __init__(self, game_server: ServerComms, name: str):
        self.game_server = game_server
        self.game_server.sendMessage(ServerMessageTypes.CREATETANK, {'Name': name})

    @staticmethod
    def get_coords(payload):
        """
        Helper function that makes a tuple of coordinates from a payload
        :param payload: Dictionary payload
        :return: The tuple of coordinates
        """
        return payload["X"], payload["Y"]

    # TODO: Method that returns a tuple of angle and distance to an object
    def distance_angle_object(self, coordinate: tuple, heading: int):
        pass

    def rx(self):
        raise NotImplementedError

    def action(self):
        raise NotImplementedError

