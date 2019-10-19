import random

from common.botinterface import BotInterface
from common.servercomms import *
from common.servermessagetypes import *


class ForwardsBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str):
        super().__init__(game_server, name)
        self.messages = []

    def rx(self):
        self.messages.append(self.game_server.readMessage())

    def action(self): # Placeholder
        self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {'Amount': random.randint(0, 10)})
