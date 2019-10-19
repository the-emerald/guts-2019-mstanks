from enum import Enum

from bot.common.botinterface import BotInterface


class CirclingBotStatuses(Enum):
    ACQUIRING, APPROACHING, CIRCLING, RETREATING = range(4)


class CirclingBot(BotInterface):
    def __init__(self):
        super(CirclingBot, self).__init__()
        self.last_message = None
        self.messages = []
        self.current_status = None

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message) # Does the updating

    def action(self):
        # Assuming the controller updates the target...
        # Acquire the target
        # Approach the target
        # Circle the target
        # If controller switches targets then retreat.
        pass
