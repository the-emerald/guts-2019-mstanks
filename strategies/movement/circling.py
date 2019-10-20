from common.servermessagetypes import ServerMessageTypes
from strategies import Strategy


class CirclingStrategy(Strategy):
    def action(self, bot):
        # Assuming the controller updates the target...
        target = bot.target  # get coordinates from target
        target_coords = (0, 0)
        dm = 150
        offset = 30
        if target:
            state = bot.tracker.positions[target]
            target_coords = state.pos
            if state.type.endswith('Pickup'):
                dm = 1
                offset = 1

        target_dist = bot.distance_to_object(target_coords)
        if target_dist < 0.1:
            return

        target_angle = bot.angle_to_object(target_coords)
        heading = (target_angle + offset + dm / target_dist) % 360
        bot.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": heading})
        bot.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})

