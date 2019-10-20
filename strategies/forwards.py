import random

from common.bot import Bot
from common.servermessagetypes import ServerMessageTypes
from strategies import Strategy


class ForwardsStrategy(Strategy):
    def action(self, bot: Bot):
        bot.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {'Amount': random.randint(0, 10)})
