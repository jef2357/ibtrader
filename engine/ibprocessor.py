#TODO:
#   Add periodic logging of input queue size 
#       every second?   5 seconds?  10 seconds?

import logging
import queue
import threading
import time

#from ibapi.utils import BadMessage, current_fn_name, read_fields
import ibapi.utils as ibutils
from ibapi.errors import *
from ibapi.common import *
import ibapi.comm as ibcomm

logger = logging.getLogger(__name__)

class ibProcessor(threading.Thread):
    def __init__(self, ib_connection, in_queue, in_queue_lock, decoder, print_lock):
        super().__init__(name = 'processor')
        self.ib_connection = ib_connection
        self.in_queue = in_queue
        self.in_queue_lock = in_queue_lock
        self.decoder = decoder
        self.print_lock = print_lock
        self.stop_event = threading.Event()

    # if you don't want to use the wrapper error method to display info  if message length is > MAX_MSG_LEN
    #   or if you use the logger for the error message, these duplicated wrapper methods are not necessary
    #
    # This is a wrapper function that is copied here so that the processor object does not need to be passed
    # a wrapper object instance when constructed
    def logAnswer(self, fnName, fnParams):
            if logger.isEnabledFor(logging.INFO):
                if 'self' in fnParams:
                    prms = dict(fnParams)
                    del prms['self']
                else:
                    prms = fnParams
                #logger.info("ANSWER %s %s", fnName, prms)
    # This is a wrapper function that is copied here so that the processor object does not need to be passed
    # a wrapper object instance when constructed
    def error(self, reqId:TickerId, errorCode:int, errorString:str, advancedOrderRejectJson = ""):
        self.logAnswer(ibutils.current_fn_name(), vars())
        if advancedOrderRejectJson:
            logger.error("ERROR %s %s %s %s", reqId, errorCode, errorString, advancedOrderRejectJson)
        else: 
            logger.error("ERROR %s %s %s", reqId, errorCode, errorString)

    # This run function to be used for the thread target is adapted from the original ib api eEClient run method
    def run(self):
        logger.debug("processor thread: thread starting")
        self.unset_stop_event()
        time1_ = time.perf_counter()

        try:
            while not self.stop_event.is_set(): # or not self.in_queue.empty():
                try:
                    try:
                        message = self.in_queue.get(block=False, timeout=0.1)
                        if len(message) > MAX_MSG_LEN:
                            logger.error("processor thread: bad message length")
                            self.error(NO_VALID_ID, BAD_LENGTH.code(), "%s:%d:%s" % (BAD_LENGTH.msg(), len(message), message))
                            logger.error("processor thread: disconnecting")
                            self.set_stop_event()
                            self.ib_connection.disconnect()
                            break
                    except queue.Empty:
                        logger.debug("in_queue empty")
                    else:
                        fields = ibcomm.read_fields(message)
                        #logger.info("fields %s", fields)
                        # this starts execution chain that ends up at wrapper handler functions
                        self.decoder.interpret(fields)    

                except ibutils.BadMessage:
                    logger.error("processor thread: bad message")
                    logger.error("processor thread: disconnecting from IB API")
                    self.set_stop_event()
                    self.ib_connection.disconnect()

                if self.in_queue.qsize() > 1000:
                    time2_ = time.perf_counter()
                    if time2_ - time1_ > 1.0:
                        logger.warning("conn:%d queue.sz:%d", self.ib_connection.isConnected(), self.in_queue.qsize())
                        print("WARNING --- Queue size > 1000 --- queue.qsize= %d", self.in_queue.qsize())
                        time1_ = time2_
        finally:
            if self.stop_event.is_set() == True:
                logger.info("processor thread: thread stopped")
            else:
                self.set_stop_event()
                logger.info("processor thread stopped")

    def set_stop_event(self):
        if self.stop_event.is_set() == False:
            self.stop_event.set()
            logger.debug("processor thread: stop event set")
        # else:
        #     logger.info("processor thread: stop event already set")

    def unset_stop_event(self):
        if self.stop_event.is_set() == True:
            self.stop_event.clear()
            logger.debug("processor thread: stop event cleared")
        # else:
        #     logger.info("processor thread: stop event already cleared")



    


            
        

