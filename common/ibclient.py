import logging
import threading
import queue
import socket
import datetime

from ibapi import comm, decoder, reader
from ibapi.client import EClient
from ibapi.server_versions import *
from ibapi.common import *
from ibapi.errors import *
from ibapi.utils import current_fn_name, BadMessage, iswrapper

from common.ibconnection import ibConnection
from engine.ibreader import ibReader
from engine.ibsender import ibSender
from engine.ibprocessor import ibProcessor


logger = logging.getLogger(__name__)


class ibClient(EClient):
    (DISCONNECTED, CONNECTING, CONNECTED, REDIRECT) = range(4)
    
    def __init__(self, wrapper):
        #EClient.__init__(self, wrapper=wrapper)
        self.wrapper = wrapper

        self.reset()
    
    @iswrapper
    def reset(self):
        self.nKeybIntHard = 0
        self.conn = None
        self.host = None
        self.port = None
        self.extraAuth = False
        self.clientId = None
        self.serverVersion_ = None
        self.connTime = None
        self.connState = None
        self.optCapab = None
        self.reader = None
        self.decoder = None
        self.setConnState(EClient.DISCONNECTED)
        self.connectionOptions = None

        self.sender = None
        self.processor = None
        self.decoder = None

        self.conn_lock = None
        self.in_queue_lock = None
        self.out_queue_lock = None
        self.print_lock = None
        self.client_lock = None
        self.req_id_lock = None
        self.in_queue = None
        self.out_queue = None
        
        self.time = datetime.datetime.now()
        self.nextValidOrderId = None

    # def setConnState() --- EClient function
    
    @iswrapper
    def sendMsg(self, msg):
        full_msg = comm.make_msg(msg)
        logger.info("%s %s %s", "SENDING", current_fn_name(1), full_msg)

        message_ququed = False
        if self.isConnected():
            with self.out_queue_lock:
                try:
                    self.out_queue.put(full_msg, block=True, timeout=0.01)
                    message_ququed = True
                except:
                    logger.error("Error writing to the output queue")
                    #return False
                finally:
                    if message_ququed:
                        logger.info("message queued: ", msg, ":", full_msg, "|", "Queue size:", self.out_queue.qsize())
                        #return True
        else:
            logger.error("Tried sending message while not connected to IB API")
            #return False

    # def logRequest() --- EClient function
    # def startApi() --- EClient function

    @iswrapper
    def connect(self, host, port, clientId):

        try:
            self.host = host
            self.port = port
            self.clientId = clientId

            logger.debug("Connecting to %s:%d w/ id:%d", self.host, self.port, self.clientId)

            self.conn_lock = threading.Lock()
            self.in_queue_lock = threading.Lock()
            self.out_queue_lock = threading.Lock()
            self.print_lock = threading.Lock()
            self.client_lock = threading.Lock()
            self.req_id_lock = threading.Lock()
            self.in_queue = queue.Queue()
            self.out_queue = queue.Queue()

            self.conn = ibConnection(self.host, self.port, self.conn_lock)
            self.conn.connect()
            self.setConnState(EClient.CONNECTING)

            v100prefix = "API\0"
            v100version = "v%d..%d" % (MIN_CLIENT_VER, MAX_CLIENT_VER)

            if self.connectionOptions:
                v100version = v100version + " " + self.connectionOptions

            #v100version = "v%d..%d" % (MIN_CLIENT_VER, 101)
            msg = comm.make_msg(v100version)
            logger.debug("ibclient.connect() msg %s", msg)
            msg2 = str.encode(v100prefix, 'ascii') + msg
            logger.debug("ibClient.connect() REQUEST %s", msg2)
            self.conn.sendMsg(msg2)

            self.decoder = decoder.Decoder(self.wrapper, self.serverVersion())
            fields = []

            #sometimes I get news before the server version, thus the loop
            while len(fields) != 2:
                self.decoder.interpret(fields)
                buf = self.conn.recvMsg()
                if not self.conn.isConnected():
                    # recvMsg() triggers disconnect() where there's a socket.error or 0 length buffer
                    # if we don't then drop out of the while loop it infinitely loops
                    logger.warning('Disconnected; resetting connection')
                    self.reset()
                    return
                logger.debug("ANSWER %s", buf)
                if len(buf) > 0:
                    (size, msg, rest) = comm.read_msg(buf)
                    logger.debug("size:%d msg:%s rest:%s|", size, msg, rest)
                    fields = comm.read_fields(msg)
                    logger.debug("fields %s", fields)
                else:
                    fields = []

            (server_version, conn_time) = fields
            server_version = int(server_version)
            logger.debug("ibClient.connect() ANSWER Version:%d time:%s", server_version, conn_time)
            self.connTime = conn_time
            self.serverVersion_ = server_version
            self.decoder.serverVersion = self.serverVersion()

            self.setConnState(EClient.CONNECTED)

            self.reader = ibReader(self.conn, self.in_queue, self.in_queue_lock, self.print_lock)            
            self.reader.start()   # start thread
            self.sender = ibSender(self.conn, self.out_queue, self.out_queue_lock, self.print_lock)
            self.sender.start()
            self.processor = ibProcessor(self.conn, self.in_queue, self.in_queue_lock, self.decoder, self.message_list, self.print_lock)

            logger.info("ibClient.connect() sent startApi")
            self.startApi()
            self.wrapper.connectAck()
        except socket.error:
            if self.wrapper:
                self.wrapper.error(NO_VALID_ID, CONNECT_FAIL.code(), CONNECT_FAIL.msg())
            logger.info("could not connect")
            self.disconnect()

    # def disconnect() --- EClient function
    # def isConnected() --- EClient function
    # def keyboardInterrupt() --- EClient function
    # def keyboardInterruptHard() --- EClient function
    # def setconnectionOptions() --- EClient function
    # def msgLoopTmo() --- EClient function
    # def msgLoopRec() --- EClient function

    @iswrapper
    def run(self):
        pass

    # def reqCurrentTime() --- EClient function
    # def serverVersion() --- EClient function
    # def setServerLogLevel() --- EClient function
    # def twsConnectionTime() --- EClient function

    ################################################################################
    # MARKET DATA FUNCTIONS
    ################################################################################

    # def reqMktData() --- EClient function



            


