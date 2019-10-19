from typing import Dict, Any

from bot.common.servermessagetypes import ServerMessageTypes
import logging


class ObjectState:
    def __init__(self, pos, heading, turret_heading, type, id, name):
        self.pos = pos
        self.heading = heading
        self.turret_heading = turret_heading
        self.type = type
        self.id = id
        self.name = name



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
            logging.info('Tracked %s at %s', name, pos)
