import logging
import threading
import queue
import socket
#import datetime
from datetime import datetime

from ibapi import comm, decoder, reader
from ibapi.client import EClient
from ibapi.server_versions import *
from ibapi.common import *
from ibapi.contract import Contract
from ibapi.errors import *
from ibapi.utils import current_fn_name, BadMessage, ClientException
from ibapi.comm import make_field, make_field_handle_empty, read_fields
from ibapi.message import OUT

from common.ibcommon import overloaded
from common.ibconnection import ibConnection
from engine.ibreader import ibReader
from engine.ibsender import ibSender
from engine.ibprocessor import ibProcessor
from engine.ibdatabase import ibDBConn

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
        self.reqid_log = None

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
        
        # self.db_config = None
        # self.db_conn = None
        # self.db_cur = None
        # self.db_cur_lock = None
        
        self.time = datetime.now()
        self.nextValidOrderId = None

        self.client_reqid_log = {}

    #def setConnState(self, connState) --- EClient function

    # New function
    def client_db_setup(self, config):
        self.client_db = ibDBConn(config)

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
                finally:
                    if message_queued:
                        logger.info("%s %s %s %s", "QUEUED (out) sendMsg(): ", full_msg, " out_queue Size: ", str(self.out_queue.qsize()))
                    else:
                        logger.error("Error putting message in out_queue")
        else:
            logger.error("Tried sending message while not connected to IB API")

    #def logRequest(self, fnName, fnParams): --- EClient function

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
            self.wrapper.wrapper_db.start()
            

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

        #TODO:
        #        Disconnect need to cancel data subscriptions so the inqueue will stop
        #        filling up
    
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
            self.wrapper.wrapper_db.set_stop_event()
            self.wrapper.wrapper_db.join()
            self.conn.disconnect()
            self.wrapper.connectionClosed()
            self.setConnState(EClient.DISCONNECTED)
            self.reset()
    
    #def isConnected(self): --- EClient function
    #def keyboardInterrupt(self): --- EClient function
    #def keyboardInterruptHard(self): --- EClient function
    #def setConectionOptions(self, options): --- EClient function

    @overloaded
    def run(self):
        pass

    def reqMktData(self, reqId:TickerId, contract:Contract,
                    genericTickList:str, snapshot:bool, regulatorySnapshot: bool,
                    mktDataOptions:TagValueList):
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

        self.logRequest(current_fn_name(), vars())

        self.client_reqid_log[reqId] = contract


        if not self.isConnected():
            self.wrapper.error(reqId, NOT_CONNECTED.code(),
                               NOT_CONNECTED.msg())
            return

        if self.serverVersion() < MIN_SERVER_VER_DELTA_NEUTRAL:
            if contract.deltaNeutralContract:
                self.wrapper.error(reqId, UPDATE_TWS.code(),
                    UPDATE_TWS.msg() + "  It does not support delta-neutral orders.")
                return

        if self.serverVersion() < MIN_SERVER_VER_REQ_MKT_DATA_CONID:
            if contract.conId > 0:
                self.wrapper.error(reqId, UPDATE_TWS.code(),
                    UPDATE_TWS.msg() + "  It does not support conId parameter.")
                return

        if self.serverVersion() < MIN_SERVER_VER_TRADING_CLASS:
            if contract.tradingClass:
                self.wrapper.error( reqId, UPDATE_TWS.code(),
                    UPDATE_TWS.msg() + "  It does not support tradingClass parameter in reqMktData.")
                return

        try:
            
            VERSION = 11
            
            # send req mkt data msg
            flds = []
            flds += [make_field(OUT.REQ_MKT_DATA),
                make_field(VERSION),
                make_field(reqId)]
    
            # send contract fields
            if self.serverVersion() >= MIN_SERVER_VER_REQ_MKT_DATA_CONID:
                flds += [make_field(contract.conId),]
    
            flds += [make_field(contract.symbol),
                make_field(contract.secType),
                make_field(contract.lastTradeDateOrContractMonth),
                make_field(contract.strike),
                make_field(contract.right),
                make_field(contract.multiplier), # srv v15 and above
                make_field(contract.exchange),
                make_field(contract.primaryExchange), # srv v14 and above
                make_field(contract.currency),
                make_field(contract.localSymbol) ] # srv v2 and above
    
            if self.serverVersion() >= MIN_SERVER_VER_TRADING_CLASS:
                flds += [make_field(contract.tradingClass),]
    
            # Send combo legs for BAG requests (srv v8 and above)
            if contract.secType == "BAG":
                comboLegsCount = len(contract.comboLegs) if contract.comboLegs else 0
                flds += [make_field(comboLegsCount),]
                for comboLeg in contract.comboLegs:
                        flds += [make_field(comboLeg.conId),
                            make_field( comboLeg.ratio),
                            make_field( comboLeg.action),
                            make_field( comboLeg.exchange)]
    
            if self.serverVersion() >= MIN_SERVER_VER_DELTA_NEUTRAL:
                if contract.deltaNeutralContract:
                    flds += [make_field(True),
                        make_field(contract.deltaNeutralContract.conId),
                        make_field(contract.deltaNeutralContract.delta),
                        make_field(contract.deltaNeutralContract.price)]
                else:
                    flds += [make_field(False),]
    
            flds += [make_field(genericTickList), # srv v31 and above
                make_field(snapshot)] # srv v35 and above
    
            if self.serverVersion() >= MIN_SERVER_VER_REQ_SMART_COMPONENTS:
                flds += [make_field(regulatorySnapshot),]
    
            # send mktDataOptions parameter
            if self.serverVersion() >= MIN_SERVER_VER_LINKING:
                #current doc says this part if for "internal use only" -> won't support it
                if mktDataOptions:
                    raise NotImplementedError("not supported")
                mktDataOptionsStr = ""
                flds += [make_field(mktDataOptionsStr),]
    
            msg = "".join(flds)
            
        except ClientException as ex:
            self.wrapper.error(reqId, ex.code, ex.msg + ex.text)
            return
        
        self.sendMsg(msg)

        # TODO:
        #   get function name and log that into the database entry with the req id
        send_time = datetime.now().isoformat()
        self.client_db.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, req_func, symbol, security_type, exchange, currency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "reqMktData", contract.symbol, contract.secType, contract.exchange, contract.currency)
        )

        pass