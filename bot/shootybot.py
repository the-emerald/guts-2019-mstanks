from bot.common.botinterface import BotInterface
from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes


class ShootyBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str):
        super().__init__(game_server, name)
        self.last_message = None

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message)
        # self.messages.append(self.game_server.readMessage())

    def action(self):
        self.game_server.sendMessage(ServerMessageTypes.TOGGLELEFT)
        if not self.last_message["messageType"] == ServerMessageTypes.OBJECTUPDATE:
            return
        target_coordinates = self.get_coords(self.last_message)
        self.game_server.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {"Amount": self.angle_to_object(
            target_coordinates)})
        self.game_server.sendMessage(ServerMessageTypes.FIRE)
