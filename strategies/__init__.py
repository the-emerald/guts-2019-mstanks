from common.bot import Bot


class Strategy:
    def __init__(self):
        self.done = False

    def action(self, bot: Bot):
        raise NotImplementedError()
