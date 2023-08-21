import logging
import queue
import threading
import time
from threading import Thread
#from threading import Thread

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

    def run(self):
        time1_ = 0.0
        try:
            while not self.stop_event.is_set(): # or not self.out_queue.empty():
                _sent = False
                if self.ib_connection.isConnected():
                    try:
                        if not self.out_queue.empty():
                            #with self.print_lock:
                            #    print("sender thread: message(s) to send, out-queue size: ", self.out_queue.qsize())

                            with self.out_queue_lock:
                                message = self.out_queue.get(block=True, timeout=0.01)
                            #with self.print_lock:
                            #   print("sender thread: Message to send: ", message, "\n")
                            while not _sent:
                                time2_ = time.perf_counter()
                                if (time2_ - time1_) > (1/(self.max_message_rate-1)):
                                    self.ib_connection.sendMsg(message)
                                    time1_ = time2_
                                    _sent = True
                                    # DEBUG print("----- sender thread: message sent to ib api --- message: ", message, ", out-queue size: ", self.out_queue.qsize())
                                else:
                                    #pass
                                    time.sleep((1/(self.max_message_rate-1) - (time2_ - time1_)))
                    except queue.Empty:
                        #print("sender thread: Out Queue is Empty")
                        pass
                else:
                    with self.print_lock:
                        print("sender thread: Not connected to IB API")
                        self.set_stop_event()
                        self.ib_connection.disconnect()
        except:
            logger.exception('sender thread: unhandled exception in ibSender thread')
            self.set_stop_event()
            self.ib_connection.disconnect()
        finally:
            with self.print_lock:
                print("sender thread: thread stopping")
            self.set_stop_event()
            self.ib_connection.disconnect()

    def set_stop_event(self):
        self.stop_event.set()
        with self.print_lock:
            print("sender thread: stop event set")

   

