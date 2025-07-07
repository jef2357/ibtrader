import logging
import time
import multiprocessing
from multiprocessing import Process
from queue import Empty

import ibapi.utils as ibutils
import ibapi.common as ibcommon
from ibapi.errors import *
from common.ibconnection import ibConnection

logger = logging.getLogger(__name__)

class ibSender(Process):
    max_message_rate = 50

    def __init__(self, ib_connection, out_queue, out_queue_lock, print_lock):
        super().__init__(name = 'sender')
        # Store connection parameters to recreate connection in process
        self.connection_host = ib_connection.host
        self.connection_port = ib_connection.port
        self.ib_connection = None  # Will be created in the process
        self.out_queue = out_queue
        self.out_queue_lock = out_queue_lock
        self.print_lock = print_lock
        self.stop_event = multiprocessing.Event()
        self.message = None

    def run(self):
        logger.debug("sender process: process starting")
        
        # Create connection within the process
        conn_lock = multiprocessing.Lock()
        self.ib_connection = ibConnection(self.connection_host, self.connection_port, conn_lock)
        try:
            self.ib_connection.connect()
        except Exception as e:
            logger.error("sender process: failed to create connection: %s", e)
            self.set_stop_event()
            return
            
        self.unset_stop_event()
        time1_ = time.perf_counter()
        try:
            while not self.stop_event.is_set(): # or not self.out_queue.empty():
                _sent = False
                if self.ib_connection.isConnected():
                    try:
                        if not self.out_queue.empty():
                            with self.out_queue_lock:
                                self.message = self.out_queue.get(block=True, timeout=0.01)
                            while not _sent:
                                time2_ = time.perf_counter()
                                if (time2_ - time1_) > (1/(self.max_message_rate-1)):
                                    self.ib_connection.sendMsg(self.message)
                                    time1_ = time2_
                                    _sent = True
                                elif time2_ - time1_ > 5:
                                    logger.error("sender process: took too long to send message to IB")
                                    break
                                else:
                                    time.sleep((1/(self.max_message_rate-1) - (time2_ - time1_)))
                            if _sent is True:
                                logger.info("%s %s %s %s","sender process: message sent:", self.message, "out-queue size: ", str(self.out_queue.qsize()))
                                self.message = None
                            else:
                                logger.error("sender process: error sending message to ib")
                    except Empty:
                        logger.debug("sender process: out queue empty")
                        pass
                else:
                    logger.error("sender process: not connected to IB API")
                    self.set_stop_event()
        except:
            logger.exception('sender process: unhandled exception in sender process')
            self.set_stop_event()
        finally:
            # Clean up connection
            if self.ib_connection:
                self.ib_connection.disconnect()
            if self.stop_event.is_set() == True:
                logger.info("sender process: process stopped")
            else:
                self.set_stop_event()
                logger.info("sender process: process stopped")

    def set_stop_event(self):
        if self.stop_event.is_set() == False:
            self.stop_event.set()
            logger.debug("sender process: stop event set")

    def unset_stop_event(self):
        if self.stop_event.is_set() == True:
            self.stop_event.clear()
            logger.debug("sender process: stop event cleared")



   

