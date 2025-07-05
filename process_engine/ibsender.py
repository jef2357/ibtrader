import logging
import queue
import threading
import time
from threading import Thread

import ibapi.utils as ibutils
import ibapi.common as ibcommon
from ibapi.errors import *

logger = logging.getLogger(__name__)

class ibSender(Thread):
    max_message_rate = 50

    def __init__(self, ib_connection, out_queue, out_queue_lock, print_lock):
        super().__init__(name = 'sender')
        self.ib_connection = ib_connection
        self.out_queue = out_queue
        self.out_queue_lock = out_queue_lock
        self.print_lock = print_lock
        self.stop_event = threading.Event()
        self.message = None

    def run(self):
        logger.debug("sender thread: thread starting")
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
                                    logger.error("sender thread: took too long to send message to IB")
                                    break
                                else:
                                    time.sleep((1/(self.max_message_rate-1) - (time2_ - time1_)))
                            if _sent is True:
                                logger.info("%s %s %s %s","sender thread: message sent:", self.message, "out-queue size: ", str(self.out_queue.qsize()))
                                self.message = None
                            else:
                                logger.error("sender thread: error sending message to ib")
                    except queue.Empty:
                        logger.debug("sender thread: out queue empty")
                        pass
                else:
                    logger.error("sender thread: not connected to IB API")
                    self.set_stop_event()
        except:
            logger.exception('sender thread: unhandled exception in sender thread')
            self.set_stop_event()
        finally:
            if self.stop_event.is_set() == True:
                logger.info("sender thread: thread stopped")
            else:
                self.set_stop_event()
                logger.info("sender thread: thread stopped")

    def set_stop_event(self):
        if self.stop_event.is_set() == False:
            self.stop_event.set()
            logger.debug("sender thread: stop event set")

    def unset_stop_event(self):
        if self.stop_event.is_set() == True:
            self.stop_event.clear()
            logger.debug("sender thread: stop event cleared")



   

