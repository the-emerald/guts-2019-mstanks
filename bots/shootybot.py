from common.botinterface import BotInterface
from common.servercomms import ServerComms
from common.servermessagetypes import ServerMessageTypes
from controller.tracker import Tracker


class ShootyBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str, tracker: Tracker):
        super().__init__(game_server, name, tracker)
        self.last_message = None
        self.sensitivity = 20

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message)
        return self.last_message

    def action(self):
        if not self.last_message:
            return
        if self.last_message["messageType"] != ServerMessageTypes.OBJECTUPDATE or \
           self.last_message["Name"] == self.name:
            return
        target_coordinates = self.get_coords(self.last_message)
        if abs(self.angle_to_object(target_coordinates) - self.heading) > self.sensitivity:
            self.game_server.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {"Amount": self.angle_to_object(
                target_coordinates)})
        self.game_server.sendMessage(ServerMessageTypes.FIRE)