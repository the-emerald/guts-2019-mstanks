#!/usr/bin/python

import json
import logging
import socket
import struct
import time

from common.servermessagetypes import ServerMessageTypes


class ServerComms(object):
    """
    TCP comms handler

    Server protocol is simple:

    * 1st byte is the message type - see ServerMessageTypes
    * 2nd byte is the length in bytes of the payload (so max 255 byte payload)
    * 3rd byte onwards is the payload encoded in JSON
    """
    ServerSocket = None
    MessageTypes = ServerMessageTypes()

    def __init__(self, hostname, port):
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSocket.connect((hostname, port))

    def readTolength(self, length):
        message_data = self.ServerSocket.recv(length)
        while len(message_data) < length:
            buff_data = self.ServerSocket.recv(length - len(message_data))
            if buff_data:
                message_data += buff_data
            # yield to other threads while waiting for more data
            time.sleep(0)
        return message_data

    def readMessage(self):
        """
        Read a message from the server
        """
        message_type_raw = self.ServerSocket.recv(1)
        message_len_raw = self.ServerSocket.recv(1)
        message_type = struct.unpack('>B', message_type_raw)[0]
        message_len = struct.unpack('>B', message_len_raw)[0]

        if message_len == 0:
            message_data = bytearray()
            message_payload = {'messageType': message_type}
        else:
            message_data = self.readTolength(message_len)
            logging.debug("*** {}".format(message_data))
            message_payload = json.loads(message_data.decode('utf-8'))
            message_payload['messageType'] = message_type

        return message_payload

    def sendMessage(self, messageType=None, messagePayload=None):
        """
        Send a message to the server
        """
        message = bytearray()

        if messageType is not None:
            message.append(messageType)
        else:
            message.append(0)

        if messagePayload is not None:
            message_string = json.dumps(messagePayload)
            message.append(len(message_string))
            message.extend(str.encode(message_string))

        else:
            message.append(0)

        return self.ServerSocket.send(message)
