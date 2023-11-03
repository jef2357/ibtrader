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
from ibapi.utils import current_fn_name, BadMessage, ClientException
from ibapi.comm import make_field, make_field_handle_empty, read_fields
from ibapi.message import OUT

from common.ibcommon import overloaded
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
    
    @overloaded
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
        self.optCapab = ""
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

        self.message_log = None

    # def setConnState(self, connState) --- EClient function
    
    @overloaded
    def sendMsg(self, msg):
        full_msg = comm.make_msg(msg)
        logger.info("%s %s %s", "SENDING", current_fn_name(1), full_msg)

        message_queued = False
        if self.isConnected():
            with self.out_queue_lock:
                try:
                    self.out_queue.put(full_msg, block=True, timeout=0.01)
                    message_queued = True
                except:
                    logger.error("Error writing to the output queue")
                    #return False
                finally:
                    if message_queued:
                        logger.info("%s %s %s %s", "QUEUED (out) sendMsg(): ", full_msg, " out_queue Size: ", str(self.out_queue.qsize()))
                    else:
                        logger.error("Error putting message in out_queue")
                        #return True
        else:
            logger.error("Tried sending message while not connected to IB API")
            #return False

    # def logRequest(self, fnName, fnParams) --- EClient function

    @overloaded
    def startApi(self):
        """  Initiates the message exchange between the client application and
        the TWS/IB Gateway. """
        # Overloaded from IB's EClient in order to directly call the sendMsg function from
        # the connection object instead of using this client's sendMsg function.  This 
        # client's sendMsg function is an overloaded definition which uses the sender queue
        # to enqueue messages for the sender thread.  Sinmpler at this point to just call
        # the connection object's sendMsg function directly here. (threads are not started)

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(),
                               NOT_CONNECTED.msg())
            return

        try: 
            
            VERSION = 2
            
            msg = make_field(OUT.START_API) \
               + make_field(VERSION)    \
               + make_field(self.clientId)
    
            if self.serverVersion() >= MIN_SERVER_VER_OPTIONAL_CAPABILITIES:
                msg += make_field(self.optCapab)
                
        except ClientException as ex:
            self.wrapper.error(NO_VALID_ID, ex.code, ex.msg + ex.text)
            return

        full_msg = comm.make_msg(msg)
        logger.info("%s %s %s", "SENDING", "startApi()", full_msg)
        self.conn.sendMsg(full_msg)

    @overloaded
    def connect(self, host, port, clientId):
        """This function must be called before any other. There is no
        feedback for a successful connection, but a subsequent attempt to
        connect will return the message \"Already connected.\"

        host:str - The host name or IP address of the machine where TWS is
            running. Leave blank to connect to the local host.
        port:int - Must match the port specified in TWS on the
            Configure>API>Socket Port field.
        clientId:int - A number used to identify this client connection. All
            orders placed/modified from this client will be associated with
            this client identifier.

            Note: Each client MUST connect with a unique clientId.
        
        For now, all threads are started in this function
        """

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
            #logger.debug("ibclient.connect() msg %s", msg)
            msg2 = str.encode(v100prefix, 'ascii') + msg
            #logger.debug("ibClient.connect() REQUEST %s", msg2)
            logger.info("%s %s %s", "SENDING connect():", current_fn_name(1), msg2)
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
            logger.info("ibClient.connect() ANSWER Version:%d time:%s", server_version, conn_time)
            self.connTime = conn_time
            self.serverVersion_ = server_version
            self.decoder.serverVersion = self.serverVersion()

            self.setConnState(EClient.CONNECTED)

            logger.info("ibClient.connect() sent startApi")
            self.startApi()
            self.wrapper.connectAck()

            self.reader = ibReader(self.conn, self.in_queue, self.in_queue_lock, self.print_lock)            
            self.sender = ibSender(self.conn, self.out_queue, self.out_queue_lock, self.print_lock)
            self.processor = ibProcessor(self.conn, self.in_queue, self.in_queue_lock, self.decoder, self.print_lock)
            self.reader.start()
            self.sender.start()
            self.processor.start()

            self.message_log = []

        except socket.error:
            if self.wrapper:
                self.wrapper.error(NO_VALID_ID, CONNECT_FAIL.code(), CONNECT_FAIL.msg())
            logger.info("could not connect")
            self.disconnect()

    @overloaded
    def disconnect(self):
        """Call this function to terminate the connections with TWS.
        Calling this function does not cancel orders that have already been
        sent."""
        while not self.in_queue.empty() or not self.out_queue.empty():
            pass
        
        if self.conn is not None:
            logger.info("disconnecting")
            self.sender.set_stop_event()
            self.sender.join()
            self.reader.set_stop_event()
            self.reader.join()
            self.processor.set_stop_event()
            self.processor.join()
            self.conn.disconnect()
            self.wrapper.connectionClosed()
            self.setConnState(EClient.DISCONNECTED)
            self.reset()
    
    # def isConnected() --- EClient function
    """Call this function to check if there is a connection with TWS"""

    # def keyboardInterrupt() --- EClient function
    #intended to be overloaded

    # def keyboardInterruptHard() --- EClient function

    # def setconnectionOptions() --- EClient function

    # def msgLoopTmo() --- EClient function
    #intended to be overloaded

    # def msgLoopRec() --- EClient function
    #intended to be overloaded

    @overloaded
    def run(self):
        pass

    # def reqCurrentTime() --- EClient function
    """Asks the current system time on the server side."""

    # def serverVersion() --- EClient function
    """Returns the version of the TWS instance to which the API
        application is connected."""
    
    # def setServerLogLevel() --- EClient function
    """The default detail level is ERROR. For more details, see API
        Logging."""
    
    # def twsConnectionTime() --- EClient function
    """Returns the time the API application made a connection to TWS."""

    ################################################################################
    # MARKET DATA FUNCTIONS
    ################################################################################

    # def reqMktData(self, reqId:TickerId, contract:Contract,
    #                genericTickList:str, snapshot:bool, regulatorySnapshot: bool,
    #                mktDataOptions:TagValueList)
    """Call this function to request market data. The market data
        will be returned by the tickPrice and tickSize events.

        reqId: TickerId - The ticker id. Must be a unique value. When the
            market data returns, it will be identified by this tag. This is
            also used when canceling the market data.
        contract:Contract - This structure contains a description of the
            Contractt for which market data is being requested.
        genericTickList:str - A commma delimited list of generic tick types.
            Tick types can be found in the Generic Tick Types page.
            Prefixing w/ 'mdoff' indicates that top mkt data shouldn't tick.
            You can specify the news source by postfixing w/ ':<source>.
            Example: "mdoff,292:FLY+BRF"
        snapshot:bool - Check to return a single snapshot of Market data and
            have the market data subscription cancel. Do not enter any
            genericTicklist values if you use snapshots.
        regulatorySnapshot: bool - With the US Value Snapshot Bundle for stocks,
            regulatory snapshots are available for 0.01 USD each.
        mktDataOptions:TagValueList - For internal use only.
            Use default value XYZ. """
    
    # def cancelMktData(self, reqId:TickerId):
    """After calling this function, market data for the specified id
        will stop flowing.

        reqId: TickerId - The ID that was specified in the call to
            reqMktData(). """
    
    # def reqMarketDataType(self, marketDataType:int):
    """The API can receive frozen market data from Trader
        Workstation. Frozen market data is the last data recorded in our system.
        During normal trading hours, the API receives real-time market data. If
        you use this function, you are telling TWS to automatically switch to
        frozen market data after the close. Then, before the opening of the next
        trading day, market data will automatically switch back to real-time
        market data.

        marketDataType:int - 1 for real-time streaming market data or 2 for
            frozen market data"""
    
    # def reqSmartComponents(self, reqId: int, bboExchange: str)

    # def reqMarketRule(self, marketRuleId: int):

    # def reqTickByTickData(self, reqId: int, contract: Contract, tickType: str,
    #                      numberOfTicks: int, ignoreSize: bool)

    # def cancelTickByTickData(self, reqId: int)

    ################################################################################
    # Options
    ################################################################################

    # def calculateImpliedVolatility(self, reqId:TickerId, contract:Contract,
    #                               optionPrice:float, underPrice:float,
    #                               implVolOptions:TagValueList):
    """Call this function to calculate volatility for a supplied
        option price and underlying price. Result will be delivered
        via EWrapper.tickOptionComputation()

        reqId:TickerId -  The request id.
        contract:Contract -  Describes the contract.
        optionPrice:double - The price of the option.
        underPrice:double - Price of the underlying."""

    # def cancelCalculateImpliedVolatility(self, reqId:TickerId):
    """Call this function to cancel a request to calculate
        volatility for a supplied option price and underlying price.

        reqId:TickerId - The request ID.  """
    
    #def calculateOptionPrice(self, reqId:TickerId, contract:Contract,
    #                         volatility:float, underPrice:float,
    #                         optPrcOptions:TagValueList):
    """Call this function to calculate option price and greek values
        for a supplied volatility and underlying price.

        reqId:TickerId -    The ticker ID.
        contract:Contract - Describes the contract.
        volatility:double - The volatility.
        underPrice:double - Price of the underlying."""
    
    #def cancelCalculateOptionPrice(self, reqId:TickerId):
    """Call this function to cancel a request to calculate the option
        price and greek values for a supplied volatility and underlying price.

        reqId:TickerId - The request ID.  """

    #def exerciseOptions(self, reqId:TickerId, contract:Contract,
    #                    exerciseAction:int, exerciseQuantity:int,
    #                    account:str, override:int):
    """reqId:TickerId - The ticker id. multipleust be a unique value.
        contract:Contract - This structure contains a description of the
            contract to be exercised
        exerciseAction:int - Specifies whether you want the option to lapse
            or be exercised.
            Values are 1 = exercise, 2 = lapse.
        exerciseQuantity:int - The quantity you want to exercise.
        account:str - destination account
        override:int - Specifies whether your setting will override the system's
            natural action. For example, if your action is "exercise" and the
            option is not in-the-money, by natural action the option would not
            exercise. If you have override set to "yes" the natural action would
             be overridden and the out-of-the money option would be exercised.
            Values are: 0 = no, 1 = yes."""
    
    ################################################################################
    # Orders
    ################################################################################

    