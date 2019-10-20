from common.servermessagetypes import ServerMessageTypes
from strategies import Strategy


class CirclingStrategy(Strategy):
    def action(self, bot):
        # Assuming the controller updates the target...
        target = bot.target  # get coordinates from target
        target_coords = (0, 0)
        if target:
            target_coords = bot.tracker.positions[target].pos

        target_dist = bot.distance_to_object(target_coords)
        if target_dist < 0.1:
            return

        target_angle = bot.angle_to_object(target_coords)
        heading = (target_angle + 30 + 150 / target_dist) % 360
        bot.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": heading})
        bot.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})

