import logging
import threading
import time
from queue import Queue, Empty
from typing import List

from common.bot import Bot
from common.servercomms import ServerComms
from controller.tracker import Tracker
from strategies.movement.circling import CirclingStrategy

from strategies.movement.goal import GoalStrategy
from strategies.turret.turretspin import TurretSpin


class Controller:
    bots: List[Bot]
    threads: List[threading.Thread]

    def __init__(self, host='127.0.0.1', port=8052, team='MELL', max_bots=4, log_level=logging.INFO, ui=True):
        logging.basicConfig(level=log_level)
        self.bots = []
        self.threads = []
        self.host = host
        self.port = port
        self.team = team
        self.max_bots = max_bots
        self.ui = ui
        self.halt = False
        self.messages = Queue()
        self.tracker = Tracker(team)

    def pick_target(self, bot):
        if bot.can_fire():
            closest = self.tracker.closest_enemy(bot)
            bot.target = closest.id if closest else None
        else:
            closest = self.tracker.closest_pickup(bot)
            bot.target = closest.id if closest else None

    def run(self):
        if self.ui:
            # local import as don't want to make tkinter load if not using it
            from controller.controllerui import ControllerUi
            ui = ControllerUi(self)
            ui_thread = threading.Thread(target=lambda: ui.start_ui(), daemon=True)
            self.threads.append(ui_thread)
            ui_thread.start()

        for i in range(0, self.max_bots):
            def _start(idx=i):
                logging.debug("Starting bot thread %s", idx)
                thread = threading.Thread(target=lambda: self.start_bot(idx), daemon=True)
                thread.start()

            _start()
            time.sleep(0.1)

        # noinspection PyBroadException
        # we need to catch everything to stop background tasks
        # we will then re raise it, so it's okay
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
                    for bot in self.bots:
                        if bot.respawn_time:
                            if bot.respawn_time < time.time():
                                bot.on_respawn()
                            continue

                        if bot.kills > 0:
                            bot.movement_strategy = GoalStrategy()

                        if bot.movement_strategy.done:
                            bot.movement_strategy = CirclingStrategy()

                        self.pick_target(bot)

        except BaseException as _:
            self.halt = True
            raise

    def start_bot(self, idx):
        def rx_loop():
            while not self.halt:
                message = bot.rx()
                self.messages.put(message)

        def turret_loop():
            while not self.halt:
                if bot.turret_strategy:
                    bot.turret_strategy.action(bot)
                time.sleep(1 / 16)

        def movement_loop():
            while not self.halt:
                if bot.movement_strategy:
                    bot.movement_strategy.action(bot)
                time.sleep(1 / 16)

        gs = ServerComms(self.host, self.port)
        bot = Bot(gs, f'{self.team}:{idx}', self.tracker)

        # TODO swap strategies as needed
        bot.movement_strategy = CirclingStrategy()
        bot.turret_strategy = TurretSpin()
        self.bots.append(bot)

        rx_thread = threading.Thread(target=rx_loop, daemon=True)
        rx_thread.start()

        turret_thread = threading.Thread(target=turret_loop, daemon=True)
        turret_thread.start()

        movement_loop()


if __name__ == '__main__':
    import fire
    import sys

    command = sys.argv[1:]
    if len(command) == 0:
        command = ["run"]
    fire.Fire(Controller, command=command)
