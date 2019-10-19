import logging

from bot.common.botinterface import BotInterface
from bot.common.servercomms import ServerComms
from bot.common.servermessagetypes import ServerMessageTypes
from bot.controller.tracker import Tracker


class CirclingBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str, tracker: Tracker):
        super(CirclingBot, self).__init__(game_server, name, tracker)
        self.last_message = None
        self.messages = []
        self.standoff_distance = 10

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message)  # Does the updating
        return self.last_message



    def action(self):
        dict {'Has points': '',
              'Aggression Level': 'High',
              'Health': self.health,
              'Ammo':self.ammo,
              'EnemyDistance':  Distance to enemies
                  Distance to health
              Distance to ammo
                  Distance to teammate
              }

        # Assuming the controller updates the target...
        target = self.target  # get coordinates from target
        if not target:
            return
        target_coords = self.tracker.positions[target].pos
        target_angle = (self.angle_to_object(target_coords) + 80) % 360
        self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": target_angle})
        self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})
        pass



