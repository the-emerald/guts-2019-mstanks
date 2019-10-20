from common.servermessagetypes import ServerMessageTypes
from strategies import Strategy

class TurretSpin(Strategy):
    def __init__(self):
        self.want_spin = 1
        self.spin = 0
        self.start = True

    def action(self, bot):
        if self.start == True:
            bot.game_server.sendMessage(ServerMessageTypes.STOPALL)
            self.start = False
        if self.want_spin == 1:
            if self.spin == 0:
                bot.game_server.sendMessage(ServerMessageTypes.TOGGLETURRETRIGHT)
                self.spin = 1
        if self.want_spin == 0:
            if self.spin == 1:
                bot.game_server.sendMessage(ServerMessageTypes.STOPTURRET)
                self.spin = 0
