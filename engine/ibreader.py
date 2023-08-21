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

    def run(self):
        try:
            buf = b""
            while not self.stop_event.is_set():
                if self.ib_connection.isConnected():
                    data = self.ib_connection.rcvMsg()
                    
                    #print("reader thread: received data ", len(data))
                    #logger.debug("reader loop, recvd size %d", len(data))
                    buf += data

                    while len(buf) > 0:
                        (size, msg, buf) = ibcomm.read_msg(buf)
                        #logger.debug("resp %s", buf.decode('ascii'))
                        #with self.lock:
                        #    print("reader thread: size: ", size, " message size: ", len(msg), " buffer: ", buf)
                        #logger.debug("size:%d msg.size:%d msg:|%s| buf:%s|", size, len(msg), buf, "|")

                        if msg:
                            with self.in_queue_lock:
                                self.in_queue.put(msg)
                            #DEBUG if not self.in_queue.empty():
                            #    with self.print_lock:
                            #        print("-o-o- reader thread: message received --- message: ", msg, ", in-queue size: ", self.in_queue.qsize())
                        else:
                            #DEBUGwith self.print_lock:
                            #    print("reader thread: more incoming packet(s) are needed")
                            logger.debug("more incoming packet(s) are needed ")
                            break
                else:
                    with self.print_lock:
                        print("reader thread: not connected to IB API")
                    pass
            
        except socket.timeout:
            with self.print_lock:
                print("reader thread: socket timeout")
                self.stop_event()
                self.ib_connection.disconnect()
        except:
            with self.print_lock:
                print("reader thread: unhandled exception")
            logger.exception('unhandled exception in ibReader thread')
            self.stop_event()
            self.ib_connection.disconnect()
        finally:
            with self.print_lock:
                print("reader thread: thread stopping")
            self.stop_event()
            self.ib_connection.disconnect()

    def set_stop_event(self, timeout=None):
        self.stop_event.set()
        with self.print_lock:
            print("reader thread: stop event set")
