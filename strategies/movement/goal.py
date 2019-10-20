import logging

from common.bot import Bot
from strategies import Strategy


class GoalStrategy(Strategy):
    def action(self, bot: Bot):
        if self.done:
            return

        logging.info("%s returning to goal", bot.name)
        bot.return_to_goal()
        bot.kills = 0
        self.done = True
        logging.info("%s returned to goal", bot.name)
