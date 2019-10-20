import logging
import time
from typing import Dict

from common.servermessagetypes import ServerMessageTypes


class ObjectState:
    STALE_TIME = 5

    def __init__(self, pos, heading, turret_heading, type, id, name):
        self.pos = pos
        self.heading = heading
        self.turret_heading = turret_heading
        self.type = type
        self.id = id
        self.name = name
        self.time = time.time()

    def is_stale(self):
        return time.time() - self.time > ObjectState.STALE_TIME


class Tracker:
    positions: Dict[str, ObjectState]

    def __init__(self):
        self.positions = {}
        self.time = 0

    def handle_message(self, message):
        if message['messageType'] == ServerMessageTypes.GAMETIMEUPDATE:
            self.time = message['Time']
        if message['messageType'] == ServerMessageTypes.OBJECTUPDATE:
            pos = message['X'], message['Y']
            heading = message['Heading']
            turret_heading = message['TurretHeading']
            name = message['Name']
            id = message['Id']
            type = message['Type']
            self.positions[id] = ObjectState(pos, heading, turret_heading, type, id, name)
            logging.debug('Tracked %s at %s', name, pos)
