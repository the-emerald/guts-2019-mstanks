import time

from common.bot import Bot
from common.servermessagetypes import ServerMessageTypes
from strategies import Strategy


class GreedyStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.standoff = 20

    def action(self, bot: Bot):
        # Assume the controller gives us a target (box) that we need to keep an eye on
        # and a do not take boxes that are deemed more important to use rather than waste
        target = bot.target  # this is an ammo box or health box
        if not target:
            return
        target_coords = bot.tracker.positions[target].pos

        # Go to standoff distance
        moved = False
        while bot.distance_to_object(target_coords) >= self.standoff:
            target_distance = bot.distance_to_object(target_coords)
            target_angle = bot.angle_to_object(target_coords)
            bot.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": target_angle})
            bot.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": target_distance})
            moved = True
            time.sleep(0.1)
        if moved:
            bot.game_server.sendMessage(ServerMessageTypes.STOPALL)
            target_coords = bot.tracker.positions[target].pos
            target_angle = (bot.angle_to_object(target_coords) + 80) % 360
            bot.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": target_angle})
            bot.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})
