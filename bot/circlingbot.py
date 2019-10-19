import logging
from enum import Enum

from bot.common.botinterface import BotInterface
from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes
from bot.controller.tracker import Tracker


class CirclingBotStatuses(Enum):
    ACQUIRING, APPROACHING, CIRCLING, RETREATING = range(4)


class CirclingBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str, tracker: Tracker):
        super(CirclingBot, self).__init__(game_server, name, tracker)
        self.last_message = None
        self.messages = []
        self.current_status = CirclingBotStatuses.ACQUIRING
        self.standoff_distance = 10

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message) # Does the updating
        return self.last_message

    def next_movement_vector(self):
        # Determine where target is
        # Create step such that step size is reasonable and angle makes it turn
        return 0, 0

    def action(self):
        # Assuming the controller updates the target...
        target = self.target  # get coordinates from target
        if not target:
            return
        logging.debug("target %s", self.target)
        target_coords = self.tracker.positions[target].pos
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
