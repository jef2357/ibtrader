import logging
import socket
import threading

from ibapi.errors import *
from ibapi.common import *
import ibapi.comm as ibcomm

logger = logging.getLogger(__name__)

class ibReader(threading.Thread):
    def __init__(self, ib_connection, in_queue, in_queue_lock, print_lock):
        super().__init__(name='reader')
        self.ib_connection = ib_connection
        self.in_queue = in_queue
        self.in_queue_lock = in_queue_lock
        self.print_lock = print_lock
        self.stop_event = threading.Event()
        self.connected_to_api = False

    def run(self):
        logger.debug("sreader thread: thread starting")
        self.unset_stop_event()
        try:
            buf = b""
            while not self.stop_event.is_set():
                if self.ib_connection.isConnected():
                    self.connected_to_api = True
                    data = self.ib_connection.recvMsg()
                    #logger.debug("reader loop, recvd size %d", len(data))
                    buf += data

                    while len(buf) > 0:
                        (size, msg, buf) = ibcomm.read_msg(buf)

                        if msg:
                            with self.in_queue_lock:
                                self.in_queue.put(msg)
                            #logger.debug("%s %s %s %s", "QUEUED (in) ibReader: ", msg, " In-Queue Size: ", str(self.in_queue.qsize()))
                        else:
                            logger.error("more incoming packet(s) are needed ")
                            break
                else:
                    if self.connected_to_api is True:
                        logger.error("reader thread: not connected to IB API")
                        self.connected_to_api = False
            
        except socket.timeout:
            self.set_stop_event()
            #self.ib_connection.disconnect()
            logger.error("reader thread: socket timeout")
        except:
            self.set_stop_event()
            #self.ib_connection.disconnect()
            logger.exception('reader thread: unhandled exception')
        finally:
            if self.stop_event.is_set() == True:
                logger.info("reader thread: thread stopped")
            else:
                self.set_stop_event()
                #self.ib_connection.disconnect()
                logger.info("reader thread: thread stopped")

    def set_stop_event(self):
        if self.stop_event.is_set() == False:
            self.stop_event.set()
            logger.debug("reader thread: stop event set")
        # else:
        #     logger.info("reader thread: stop event already set")

    def unset_stop_event(self):
        if self.stop_event.is_set() == True:
            self.stop_event.clear()
            logger.debug("reader thread: stop event cleared")
        # else:
        #     logger.info("reader thread: stop event already cleared")

