from common.servermessagetypes import ServerMessageTypes
from strategies import Strategy


class TurretSpin(Strategy):
    def __init__(self):
        self.want_spin = True
        self.spin = False
        self.start = True

    def action(self, bot):
        if self.start:
            bot.game_server.sendMessage(ServerMessageTypes.STOPALL)
            self.start = False
        if self.want_spin and not self.spin:
            bot.game_server.sendMessage(ServerMessageTypes.TOGGLETURRETRIGHT)
            self.spin = True
        if not self.want_spin and self.spin:
            bot.game_server.sendMessage(ServerMessageTypes.STOPTURRET)
            self.spin = False
