import threading
import time
from typing import List

from bot.common.botinterface import BotInterface
from bot.common.servercomms import ServerComms
from bot.shootybot import ShootyBot


class Controller:
    bots: List[BotInterface]

    def __init__(self, host='127.0.0.1', port=8052, team='MELL', max_bots=4):
        self.bots = []
        self.host = host
        self.port = port
        self.team = team
        self.max_bots = max_bots
        self.halt = False

    def run(self):
        for i in range(0, self.max_bots):
            def _start(idx=i):
                print(f"Spawning bot {idx}")
                thread = threading.Thread(target=lambda: self.start_bot(idx))
                thread.start()

            _start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.halt = True

    def start_bot(self, idx):
        gs = ServerComms(self.host, self.port)
        bot = ShootyBot(gs, f'{self.team}:{idx}')
        self.bots.append(bot)
        while not self.halt:
            bot.rx()
            bot.action()
            time.sleep(1/16)


if __name__ == '__main__':
    import fire
    import sys

    command = sys.argv[1:]
    if len(command) == 0:
        command = ["run"]
    fire.Fire(Controller, command=command)
