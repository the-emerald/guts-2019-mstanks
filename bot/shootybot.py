from bot.common.botinterface import BotInterface
from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes


class ShootyBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str):
        super().__init__(game_server, name)
        self.last_message = None

    # TODO: Method that determines whether the turret should turn left or right on a target. Should return either
    #   ServerMessageTypes left or right
    def determine_turret_turn_angle(self, coordinate: tuple):
        pass

    def rx(self):
        self.last_message = self.game_server.readMessage()
        # self.messages.append(self.game_server.readMessage())

    def action(self):
        if not self.last_message["messageType"] == 18:
            return
        target_coordinates = self.get_coords(self.last_message)
        self.game_server.sendMessage(self.determine_turret_turn_angle(target_coordinates))
        self.game_server.sendMessage(ServerMessageTypes.FIRE)

