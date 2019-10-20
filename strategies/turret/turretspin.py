import time

from common.servermessagetypes import ServerMessageTypes
from strategies import Strategy


class TurretSpin(Strategy):
    def __init__(self):
        self.want_spin = True
        self.spin = False
        self.start = True

    def action(self, bot):
        if self.start:
            bot.game_server.sendMessage(ServerMessageTypes.STOPTURRET)
            self.start = False
        if self.want_spin and not self.spin:
            bot.game_server.sendMessage(ServerMessageTypes.TOGGLETURRETRIGHT)
            self.spin = True
        if not self.want_spin and self.spin:
            bot.game_server.sendMessage(ServerMessageTypes.STOPTURRET)
            self.spin = False

        if bot.target and bot.can_fire():
            position = bot.tracker.positions[bot.target]
            if not position.is_stale():
                # todo targetting

                firing_angle = bot.angle_to_object(position.pos)
                bot.turn_turret_to_heading(firing_angle)
                dist = bot.distance_to_object(position.pos)

                angle_deviation = abs(bot.turret_heading - firing_angle)

                if dist < 30 and angle_deviation < (100/dist):
                    bot.fire()
