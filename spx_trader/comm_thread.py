import logging
import queue
import threading
import time
import zmq

logger = logging.getLogger(__name__)

class interProcessComm(threading.Thread):
    def __init__(self, mode=None):
        super().__init__(name = 'ipc')
        self.stop_event = threading.Event()

        context = zmq.Context()
        
        match mode:
            case "SUB"
                self.socket = context.socket(zmq.SUB)
                try:
                    self.socket.connect("tcp://localhost:5555")
                    self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
                except zmq.error.ZMQError as e:
                    logger.error("ipc thread: zmq error: %s", e)
            case "PUB"
                self.socket = context.socket(zmq.PUB)
                try:
                    self.socket.bind("tcp://*:5555")
                except zmq.error.ZMQError as e:
                    logger.error("ipc thread: zmq error: %s", e)

    

    def run(self):
        pass

    def set_stop_event(self):
        if self.stop_event.is_set() == False:
            self.stop_event.set()
            logger.debug("ipc thread: stop event set")

    def unset_stop_event(self):
        if self.stop_event.is_set() == True:
            self.stop_event.clear()
            logger.debug("ipc thread: stop event cleared")




