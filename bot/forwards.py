import random

from bot.common.botinterface import InterfaceBot
from bot.common.servercomms import *
from bot.common.servermessagetypes import *


class ForwardsBot(InterfaceBot):
    def __init__(self, game_server: ServerComms, name: int):
        super().__init__(game_server, name)
        self.messages = []

    def rx(self):
        self.messages.append(self.game_server.readMessage())

    def action(self): # Placeholder
        self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {'Amount': random.randint(0, 10)})
