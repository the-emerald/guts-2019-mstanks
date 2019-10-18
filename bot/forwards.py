import random

from bot.interfacebot import InterfaceBot
from bot.servercomms import *
from bot.servermessagetypes import *


class ForwardsBot(InterfaceBot):
    def __init__(self, game_server: ServerComms, name: int):
        super().__init__(game_server, name)
        self.messages = []

    def rx(self):
        self.messages.append(self.game_server.readMessage())

    def move(self): # Placeholder
        self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {'Amount': random.randint(0, 10)})
