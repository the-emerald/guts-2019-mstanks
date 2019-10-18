from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes


class BotInterface:
    def __init__(self, game_server: ServerComms, name: str):
        self.game_server = game_server
        self.game_server.sendMessage(ServerMessageTypes.CREATETANK, {'Name': name})

    # TODO: Method that returns a tuple of angle and distance to an object
    def distance_angle_object(self, coordinate: tuple, heading: int):
        pass

    def rx(self):
        raise NotImplementedError

    def action(self):
        raise NotImplementedError

