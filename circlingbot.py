from enum import Enum

from bot.common.botinterface import BotInterface
from bot.common.servermessagetypes import ServerMessageTypes


class CirclingBotStatuses(Enum):
    ACQUIRING, APPROACHING, CIRCLING, RETREATING = range(4)


class CirclingBot(BotInterface):
    def __init__(self):
        super(CirclingBot, self).__init__()
        self.last_message = None
        self.messages = []
        self.current_status = CirclingBotStatuses.ACQUIRING
        self.standoff_distance = 10

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message) # Does the updating

    def next_movement_vector(self):
        # Determine where target is
        # Create step such that step size is reasonable and angle makes it turn
        return 0, 0

    def action(self):
        # Assuming the controller updates the target...
        target_coords = (0, 0)   # TODO: Implement a way to get target coordinates
        target_angle = self.angle_to_object(target_coords)
        self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": target_angle})
        if self.current_status == CirclingBotStatuses.ACQUIRING and self.heading == target_angle:
            # ^^ may need a "good-enough" filter
            self.current_status = CirclingBotStatuses.APPROACHING

        # Approach the target
        if self.current_status == CirclingBotStatuses.APPROACHING:
            while self.distance_to_object(target_coords) <= self.standoff_distance:
                self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 9000})
            self.game_server.sendMessage(ServerMessageTypes.STOPALL)
            self.current_status = CirclingBotStatuses.CIRCLING

        if self.current_status == CirclingBotStatuses.CIRCLING:
            move_distance, move_degree = self.next_movement_vector()


        # Circle the target
        # If controller switches targets then retreat.
        pass
