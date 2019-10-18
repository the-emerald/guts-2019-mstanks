import random
from bot.servercomms import *
from bot.servermessagetypes import ServerMessageTypes


class EmeraldBot:
    def __init__(self, game_server: ServerComms, name: int):
        self.game_server = game_server
        self.game_server.sendMessage(ServerMessageTypes.CREATETANK, {'Name': name})

    def forward_thing(self): # Placeholder
        self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {'Amount': random.randint(0, 10)})
