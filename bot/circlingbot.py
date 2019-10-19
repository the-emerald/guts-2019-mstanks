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
        target_coords = self.tracker.positions[target].pos
        target_angle = (self.angle_to_object(target_coords) + 80) % 360
        self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": target_angle})
        self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})

        # Circle the target
        # If controller switches targets then retreat.
        pass
