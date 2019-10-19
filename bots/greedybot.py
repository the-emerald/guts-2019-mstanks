from common.botinterface import BotInterface
from common.servercomms import ServerComms
from common.servermessagetypes import ServerMessageTypes
from controller.tracker import Tracker


class GreedyBot(BotInterface):
    def __init__(self, game_server: ServerComms, name: str, tracker: Tracker):
        super().__init__(game_server, name, tracker)
        self.last_message = None
        self.do_not_take_boxes = []  # TODO: Update fat controller to determine and update this
        self.standoff = 20
        self.trigger = 25

    def rx(self):
        self.last_message = self.game_server.readMessage()
        self.handle_message(self.last_message)  # Does the updating
        return self.last_message

    def action(self):
        # Assume the controller gives us a target (box) that we need to keep an eye on
        # and a do not take boxes that are deemed more important to use rather than waste
        target = self.target  # this is an ammo box or health box
        if not target:
            return
        target_coords = self.tracker.positions[target].pos
        target_distance = self.distance_to_object(target_coords)
        target_angle = self.angle_to_object(target_coords)

        # Go to standoff distance
        moved = False
        while self.distance_to_object(target_coords) >= self.standoff:
            self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": target_angle})
            self.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": target_distance})
            moved = True
        if moved:
            self.game_server.sendMessage(ServerMessageTypes.STOPALL)

        # TODO: Make the bot orbit (still haven't figured out how to out it)
        # TODO: If an enemy bot is spotted inside the trigger range, and it is low on health, then run towards the box




