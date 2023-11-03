"""
Copyright (C) 2019 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
 and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""


"""
Just a thin wrapper around a socket.
It allows us to keep some other info along with it.
"""


import socket
#import threading
import logging
import sys
from ibapi.errors import FAIL_CREATE_SOCK
from ibapi.errors import CONNECT_FAIL
from ibapi.common import NO_VALID_ID


#TODO: support SSL !!

logger = logging.getLogger(__name__)


class ibConnection:
    def __init__(self, host, port, connection_lock, wrapper=None):
        self.host = host
        self.port = port
        self.socket = None
        self.wrapper = wrapper
        self.lock = connection_lock

    # OVERLOADED from ib's connection.py
    def connect(self):
        logger.debug("ibconnection.connect() Acquiring connection lock")
        with self.lock:
            try:
                logger.debug("Attempting to create socket")
                self.socket = socket.socket()
            #TODO: list the exceptions you want to catch
            except socket.error:
                logger.error("Error creating to socket")
                if self.wrapper:
                    self.wrapper.error(NO_VALID_ID, FAIL_CREATE_SOCK.code(), FAIL_CREATE_SOCK.msg())
            else:
                logger.debug("Succesfully created socket")

            try:
                logger.debug("Attempting to connect to socket " + str(self.host)+":"+str(self.port))
                self.socket.connect((self.host, self.port))
            except socket.error:
                logger.error("Error connecting to socket " + str(self.host)+":"+str(self.port))
                if self.wrapper:
                    self.wrapper.error(NO_VALID_ID, CONNECT_FAIL.code(), CONNECT_FAIL.msg())
            else:
                logger.debug("Succesfully connected to socket " + str(self.host)+":"+str(self.port))

            self.socket.settimeout(1)   #non-blocking
        logger.debug("ibconnection.connect() released connection lock")

    def disconnect(self):
        #logger.debug("ibconnection.disconnect() Acquiring connection lock")
        with self.lock:
            try:
                if self.socket is not None:
                    logger.debug("disconnecting")
                    self.socket.close()
                    self.socket = None
                    logger.debug("disconnected")
                    if self.wrapper:
                        self.wrapper.connectionClosed()
                else:
                    logger.error("No socket exists to close")
            except:
                logger.error("Error closing socket")
        logger.debug("ibconnection.disconnect() released connection lock")

    def isConnected(self):
        return self.socket is not None

    def sendMsg(self, msg):
        logger.debug("ibconnection.sendMsg acquiring connection lock")
        with self.lock:
            if not self.isConnected():
                logger.debug("sendMsg attempted while not connected, releasing lock")
                #self.lock.release()
                return 0
            try:
                nSent = self.socket.send(msg)
            except socket.error:
                logger.error("exception from ibConnection.sendMsg %s", sys.exc_info())
                raise
            finally:
                pass
                #logger.debug("ibconnection.sendMsg releasing lock")

            logger.debug("ibconnection.sendMsg: sent: %d", nSent)
        logger.debug("ibconnection.sendMsg released connection lock")
        return nSent

    def recvMsg(self):
        if not self.isConnected():
            logger.debug("recvMsg attempted while not connected, releasing lock")
            return b""
        try:
            buf = self._recvAllMsg()
            # receiving 0 bytes outside a timeout means the connection is either
            # closed or broken
            if len(buf) == 0:
                logger.debug("socket either closed or broken, disconnecting")
                self.disconnect()
        except socket.timeout:
            logger.debug("socket timeout from recvMsg %s", sys.exc_info())
            buf = b""
        except socket.error:
            logger.debug("socket broken, disconnecting")
            self.disconnect()
            buf = b""
        except OSError:
            # Thrown if the socket was closed (ex: disconnected at end of script) 
            # while waiting for self.socket.recv() to timeout.
            logger.error("Socket is broken or closed.")

        return buf

    def _recvAllMsg(self):
        _continue = True
        _all_buffer = b""

        while _continue and self.isConnected():
            _buffer = self.socket.recv(4096)
            _all_buffer += _buffer
            logger.debug("len %d raw:%s|", len(_buffer), _buffer)

            if len(_buffer) < 4096:
                _continue = False

        return _all_buffer

