import logging
import threading
import time
from queue import Queue, Empty
from typing import List

from common.bot import Bot
from common.servercomms import ServerComms
from controller.tracker import Tracker
from strategies.circling import CirclingStrategy


class Controller:
    bots: List[Bot]

    def __init__(self, host='127.0.0.1', port=8052, team='MELL', max_bots=4):
        self.bots = []
        self.host = host
        self.port = port
        self.team = team
        self.max_bots = max_bots
        self.halt = False
        self.messages = Queue()
        self.tracker = Tracker()

    def run(self):
        for i in range(0, self.max_bots):
            def _start(idx=i):
                print(f"Spawning bot {idx}")
                thread = threading.Thread(target=lambda: self.start_bot(idx))
                thread.start()

            _start()

        try:
            last_time = time.time()
            while True:
                try:
                    message = self.messages.get(timeout=2)
                    logging.debug('Message %s', message)
                    self.tracker.handle_message(message)
                except Empty:
                    pass

                cur_time = time.time()
                logging.debug("time %s last_time %s", cur_time, last_time)
                if cur_time - last_time > 1:
                    last_time = cur_time

                    targ = None
                    for entity_id, state in self.tracker.positions.items():
                        if state.type == 'AmmoPickup' and not state.name.startswith(self.team + ':'):
                            targ = entity_id

                    for bot in self.bots:
                        bot.target = targ
                    logging.debug("Target: %s", targ)
        except KeyboardInterrupt:
            self.halt = True

    def start_bot(self, idx):
        def rx_thread():
            while not self.halt:
                message = bot.rx()
                self.messages.put(message)

        gs = ServerComms(self.host, self.port)
        bot = Bot(gs, f'{self.team}:{idx}', self.tracker)
        # TODO swap strategies as needed
        bot.strategy = CirclingStrategy()
        self.bots.append(bot)

        threading.Thread(target=rx_thread).start()
        while not self.halt:
            bot.action()
            time.sleep(1 / 16)


if __name__ == '__main__':
    import fire
    import sys

    logging.basicConfig(level=logging.DEBUG)
    command = sys.argv[1:]
    if len(command) == 0:
        command = ["run"]
    fire.Fire(Controller, command=command)
