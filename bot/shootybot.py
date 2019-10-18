from bot.common.botinterface import BotInterface
from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes


class ShootyBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str):
        super().__init__(game_server, name)
        self.last_message = None

    # TODO: Method that determines whether the tank should turn left or right on a target. Should return either
    #   ServerMessageTypes left or right
    def determine_turn_angle(self, angle: int):
        pass

    def rx(self):
        self.last_message = self.game_server.readMessage()
        # self.messages.append(self.game_server.readMessage())

    def action(self):
        if not self.last_message["messageType"] == 18:
            return
        distance, angle = self.distance_angle_object(self.get_coords(self.last_message), self.last_message["Heading"])

        self.game_server.sendMessage(ServerMessageTypes.FIRE)

