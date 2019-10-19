import logging

from bot.common.botinterface import BotInterface
from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes
from bot.controller.tracker import Tracker


class GoalBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str, tracker: Tracker):
        super(GoalBot, self).__init__(game_server, name, tracker)
        self.last_message = None
        self.messages = []
        self.standoff_distance = 10

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message)  # Does the updating
        return self.last_message

    def action(self):
        while True:
            self.return_to_goal()
        pass
