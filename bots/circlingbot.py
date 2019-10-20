from common.botinterface import BotInterface
from common.servercomms import ServerComms
from common.servermessagetypes import ServerMessageTypes
from controller.tracker import Tracker


class CirclingBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str, tracker: Tracker):
        super(CirclingBot, self).__init__(game_server, name, tracker)
        self.last_message = None
        self.messages = []
        self.standoff_distance = 10

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message)  # Does the updating
        return self.last_message

    def action(self):
        # Assuming the controller updates the target...
        target = self.target  # get coordinates from target
        if not target:
            return
        target_coords = self.tracker.positions[target].pos
        target_dist = self.distance_to_object(target_coords)
        target_angle = self.angle_to_object(target_coords)
        heading = (target_angle + 45 + 45 / target_dist) % 360
        self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": heading})
        self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})
        pass
