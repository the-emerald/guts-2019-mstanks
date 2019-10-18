from bot.common.botinterface import InterfaceBot
from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes


class ShootyBot(InterfaceBot):

    def __init__(self, game_server: ServerComms, name: int):
        super().__init__(game_server, name)
        self.last_message = None

    def rx(self):
        self.last_message = self.game_server.readMessage()
        # self.messages.append(self.game_server.readMessage())

    def action(self):
        if not self.last_message["messageType"] == 18:
            return
        self.game_server.sendMessage(ServerMessageTypes.FIRE)


