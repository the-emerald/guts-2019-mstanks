import logging

from common import targeting
from common.servermessagetypes import ServerMessageTypes
from controller.tracker import Alignment, ObjectState
from strategies import Strategy


class TurretSpin(Strategy):
    def __init__(self):
        super().__init__()
        self.want_spin = True
        self.spin = False
        self.start = True

    def try_shoot(self, bot):
        if bot.target and bot.ammo > 0:
            tgt: ObjectState = bot.tracker.positions[bot.target]
            if not tgt.is_stale() and (tgt.alignment == Alignment.FOE or tgt.alignment == Alignment.FRIEND and tgt.health == 1):
                dist = bot.distance_to_object(tgt.pos)
                if dist > 30:
                    return False
                if dist == 0:
                    dist = 0.1

                if not bot.can_fire():
                    return True

                if self.spin:
                    bot.game_server.sendMessage(ServerMessageTypes.STOPTURRET)
                    self.spin = False
                firing_angle = targeting.calculate_firing_solution(tgt.pos, tgt)

                if not firing_angle:
                    firing_angle = bot.angle_to_object(tgt.pos)

                bot.turn_turret_to_heading(firing_angle)

                angle_deviation = abs(bot.turret_heading - firing_angle)

                if dist < 30 and angle_deviation < (100 / dist):
                    bot.fire()

                return True
        return False

    def action(self, bot):
        trying_to_shoot = self.try_shoot(bot)
        self.want_spin = not trying_to_shoot

        if self.start:
            bot.game_server.sendMessage(ServerMessageTypes.STOPTURRET)
            self.start = False
        if self.want_spin and not self.spin:
            bot.game_server.sendMessage(ServerMessageTypes.TOGGLETURRETRIGHT)
            self.spin = True
        if not self.want_spin and self.spin:
            bot.game_server.sendMessage(ServerMessageTypes.STOPTURRET)
            self.spin = False
