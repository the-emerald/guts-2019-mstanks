from common.bot import Bot
from strategies import Strategy


class GoalStrategy(Strategy):
    def action(self, bot: Bot):
        bot.return_to_goal()
