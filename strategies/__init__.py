from common.bot import Bot


class Strategy:
    def action(self, bot: Bot):
        raise NotImplementedError()
