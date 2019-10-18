from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes


class InterfaceBot:
    def __init__(self, game_server: ServerComms, name: int):
        self.game_server = game_server
        self.game_server.sendMessage(ServerMessageTypes.CREATETANK, {'Name': name})

    def rx(self):
        raise NotImplementedError

    def move(self):
        raise NotImplementedError

