from common.bot import Bot
from common.servermessagetypes import ServerMessageTypes
from strategies import Strategy


class ShootyStrategy(Strategy):
    def __init__(self):
        self.sensitivity = 20

    def action(self, bot: Bot):
        if not bot.target:
            return
        target_coordinates = bot.tracker.positions[bot.target].pos
        if abs(bot.angle_to_object(target_coordinates) - bot.heading) > self.sensitivity:
            bot.game_server.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {"Amount": bot.angle_to_object(
                target_coordinates)})
        bot.game_server.sendMessage(ServerMessageTypes.FIRE)
