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
#from engine.ibdatabase import ibDBConn
from database_spx_trader import spxTraderDBConn

logger = logging.getLogger(__name__)


class   spxTraderClient(EClient):
    (DISCONNECTED, CONNECTING, CONNECTED, REDIRECT) = range(4)
    
    def __init__(self, wrapper, db_conn:spxTraderDBConn):
        EClient.__init__(self, wrapper=wrapper)
        self.wrapper = wrapper
        self.db_conn = db_conn
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

        self.conn_lock = threading.Lock()
        self.in_queue_lock = threading.Lock()
        self.out_queue_lock = threading.Lock()
        self.print_lock = threading.Lock()
        self.client_lock = threading.Lock()
        
        #TODO: investigate using priority queye for the in and out queues
        self.in_queue = queue.Queue()
        self.out_queue = queue.Queue()

        if self.host and self.port and self.clientId:
            self.conn = ibConnection(self.host, self.port, self.conn_lock)
            self.reader = ibReader(self.conn, self.in_queue, self.in_queue_lock, self.print_lock)            
            self.sender = ibSender(self.conn, self.out_queue, self.out_queue_lock, self.print_lock)
            self.processor = ibProcessor(self.conn, self.in_queue, self.in_queue_lock, self.decoder, self.print_lock)

    @overloaded
    def sendMsg(self, msg, client_func=None):
        full_msg = comm.make_msg(msg)
        logger.info("%s %s %s", "SENDING", current_fn_name(1), full_msg)

        message_queued = False
        if self.isConnected():
            with self.out_queue_lock:
                try:
                    self.out_queue.put(full_msg, block=False, timeout=0.01)
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

            self.conn = ibConnection(self.host, self.port, self.conn_lock)

            logger.debug("Connecting to %s:%d w/ id:%d", self.host, self.port, self.clientId)

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
            
            self.db_conn.start()
            self.processor.start()
            self.reader.start()
            self.sender.start()

            self.reqIds(1)

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
            if self.sender.is_alive(): self.sender.join()
            self.reader.set_stop_event()
            if self.reader.is_alive(): self.reader.join()
            self.processor.set_stop_event()
            if self.processor.is_alive(): self.processor.join()
            self.db_conn.set_stop_event()
            if self.db_conn.is_alive(): self.db_conn.join()
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

    @overloaded
    def reqIds(self, numIds:int):
        """Call this function to request from TWS the next valid ID that
        can be used when placing an order.  After calling this function, the
        nextValidId() event will be triggered, and the id returned is that next
        valid ID. That ID will reflect any autobinding that has occurred (which
        generates new IDs and increments the next valid ID therein).

        numIds:int - deprecated"""

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        VERSION = 1

        msg = make_field(OUT.REQ_IDS) \
           + make_field(VERSION)   \
           + make_field(numIds)

        self.sendMsg(msg, "reqIds")

        # TODO:
        #   get function name and log that into the database entry with the req id
        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, send_time, caller_func, caller_id) VALUES (%s, %s, %s, %s)",
            ("ib_api", send_time, "reqIds", OUT.REQ_IDS)
        )

    @overloaded
    def reqContractDetails(self, reqId:int , contract:Contract):
        """Call this function to download all details for a particular
        underlying. The contract details will be received via the contractDetails()
        function on the EWrapper.

        reqId:int - The ID of the data request. Ensures that responses are
            make_fieldatched to requests if several requests are in process.
        contract:Contract - The summary description of the contract being looked
            up."""

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        if self.serverVersion() < MIN_SERVER_VER_SEC_ID_TYPE:
            if contract.secIdType or contract.secId:
                self.wrapper.error( reqId, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                        "  It does not support secIdType and secId parameters.")
                return

        if self.serverVersion() < MIN_SERVER_VER_TRADING_CLASS:
            if contract.tradingClass:
                self.wrapper.error( reqId, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                        "  It does not support tradingClass parameter in reqContractDetails.")
                return

        if self.serverVersion() < MIN_SERVER_VER_LINKING:
            if contract.primaryExchange:
                self.wrapper.error( reqId, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                        "  It does not support primaryExchange parameter in reqContractDetails.")
                return

        if self.serverVersion() < MIN_SERVER_VER_BOND_ISSUERID:
            if contract.issuerId:
                self.wrapper.error( reqId, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                        "  It does not support issuerId parameter in reqContractDetails.")
                return

        try:
            
            VERSION = 8

            # send req mkt data msg
            flds = []
            flds += [make_field(OUT.REQ_CONTRACT_DATA),
                make_field( VERSION)]

            if self.serverVersion() >= MIN_SERVER_VER_CONTRACT_DATA_CHAIN:
                flds += [make_field( reqId),]

            # send contract fields
            flds += [make_field(contract.conId), # srv v37 and above
                make_field(contract.symbol),
                make_field(contract.secType),
                make_field(contract.lastTradeDateOrContractMonth),
                make_field(contract.strike),
                make_field(contract.right),
                make_field(contract.multiplier)] # srv v15 and above

            if self.serverVersion() >= MIN_SERVER_VER_PRIMARYEXCH:
                flds += [make_field(contract.exchange),
                    make_field(contract.primaryExchange)]
            elif self.serverVersion() >= MIN_SERVER_VER_LINKING:
                if (contract.primaryExchange and
                    (contract.exchange == "BEST" or contract.exchange == "SMART")):
                    flds += [make_field(contract.exchange + ":" + contract.primaryExchange),]
                else:
                    flds += [make_field(contract.exchange),]

            flds += [make_field( contract.currency),
                make_field( contract.localSymbol)]
            if self.serverVersion() >= MIN_SERVER_VER_TRADING_CLASS:
                flds += [make_field(contract.tradingClass), ]
            flds += [make_field(contract.includeExpired),] # srv v31 and above

            if self.serverVersion() >= MIN_SERVER_VER_SEC_ID_TYPE:
                flds += [make_field( contract.secIdType),
                    make_field( contract.secId)]

            if self.serverVersion() >= MIN_SERVER_VER_BOND_ISSUERID:
                flds += [make_field(contract.issuerId), ]

            msg = "".join(flds)
        
        except ClientException as ex:
            self.wrapper.error(reqId, ex.code, ex.msg + ex.text)
            return

        self.sendMsg(msg)

        # TODO:
        #   get function name and log that into the database entry with the req id
        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id, symbol, security_type, exchange, currency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "reqMktData", OUT.REQ_CONTRACT_DATA, contract.symbol, contract.secType, contract.exchange, contract.currency)
        )

    @overloaded
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

        #TODO:  Is this implemented anywhere?
        #self.client_reqid_log[reqId] = contract


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
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id, symbol, security_type, exchange, currency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "reqMktData", OUT.REQ_MKT_DATA, contract.symbol, contract.secType, contract.exchange, contract.currency)
        )

        pass

    @overloaded
    def cancelMktData(self, reqId:TickerId):
        """After calling this function, market data for the specified id
        will stop flowing.

        reqId: TickerId - The ID that was specified in the call to
            reqMktData(). """

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(reqId, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        VERSION = 2

        # send req mkt data msg
        flds = []
        flds += [make_field(OUT.CANCEL_MKT_DATA),
            make_field(VERSION),
            make_field(reqId)]

        msg = "".join(flds)
        self.sendMsg(msg)

        # TODO:
        #   get function name and log that into the database entry with the req id
        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id) VALUES (%s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "cancelMktData", OUT.CANCEL_MKT_DATA)
        )

    @overloaded
    def reqTickByTickData(self, reqId: int, contract: Contract, tickType: str,
                          numberOfTicks: int, ignoreSize: bool):
        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        if self.serverVersion() < MIN_SERVER_VER_TICK_BY_TICK:
            self.wrapper.error(NO_VALID_ID, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                               " It does not support tick-by-tick data requests.")
            return

        if self.serverVersion() < MIN_SERVER_VER_TICK_BY_TICK_IGNORE_SIZE:
            self.wrapper.error(NO_VALID_ID, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                               " It does not support ignoreSize and numberOfTicks parameters "
                               "in tick-by-tick data requests.")
            return

        try:
            
            msg = make_field(OUT.REQ_TICK_BY_TICK_DATA)\
                + make_field(reqId) \
                + make_field(contract.conId) \
                + make_field(contract.symbol) \
                + make_field(contract.secType) \
                + make_field(contract.lastTradeDateOrContractMonth) \
                + make_field(contract.strike) \
                + make_field(contract.right) \
                + make_field(contract.multiplier) \
                + make_field(contract.exchange) \
                + make_field(contract.primaryExchange) \
                + make_field(contract.currency) \
                + make_field(contract.localSymbol) \
                + make_field(contract.tradingClass) \
                + make_field(tickType)
    
            if self.serverVersion() >= MIN_SERVER_VER_TICK_BY_TICK_IGNORE_SIZE:
                msg += make_field(numberOfTicks) \
                    + make_field(ignoreSize)

        except ClientException as ex:
            self.wrapper.error(reqId, ex.code, ex.msg + ex.text)
            return

        self.sendMsg(msg)

        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id, symbol, security_type, exchange, currency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "reqTickByTickData", OUT.REQ_TICK_BY_TICK_DATA, contract.symbol, contract.secType, contract.exchange, contract.currency)
        )

    @overloaded
    def cancelTickByTickData(self, reqId: int):
        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        if self.serverVersion() < MIN_SERVER_VER_TICK_BY_TICK:
            self.wrapper.error(NO_VALID_ID, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                               " It does not support tick-by-tick data requests.")
            return

        msg = make_field(OUT.CANCEL_TICK_BY_TICK_DATA) \
            + make_field(reqId)

        self.sendMsg(msg)

        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, CALLER_ID) VALUES (%s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "cancelTickByTickData", OUT.CANCEL_TICK_BY_TICK_DATA)
        )

    @overloaded
    def reqRealTimeBars(self, reqId:TickerId, contract:Contract, barSize:int,
                        whatToShow:str, useRTH:bool,
                        realTimeBarsOptions:TagValueList):
        """Call the reqRealTimeBars() function to start receiving real time bar
        results through the realtimeBar() EWrapper function.

        reqId:TickerId - The Id for the request. Must be a unique value. When the
            data is received, it will be identified by this Id. This is also
            used when canceling the request.
        contract:Contract - This object contains a description of the contract
            for which real time bars are being requested
        barSize:int - Currently only 5 second bars are supported, if any other
            value is used, an exception will be thrown.
        whatToShow:str - Determines the nature of the data extracted. Valid
            values include:
            TRADES
            BID
            ASK
            MIDPOINT
        useRTH:bool - Regular Trading Hours only. Valid values include:
            0 = all data available during the time span requested is returned,
                including time intervals when the market in question was
                outside of regular trading hours.
            1 = only data within the regular trading hours for the product
                requested is returned, even if the time time span falls
                partially or completely outside.
        realTimeBarOptions:TagValueList - For internal use only. Use default value XYZ."""

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        if self.serverVersion() < MIN_SERVER_VER_TRADING_CLASS:
            if contract.tradingClass:
                self.wrapper.error( reqId, UPDATE_TWS.code(),
                    UPDATE_TWS.msg() + "  It does not support conId and tradingClass parameter in reqRealTimeBars.")
                return

        try:
                
            VERSION = 3
    
            flds = []
            flds += [make_field(OUT.REQ_REAL_TIME_BARS),
                make_field(VERSION),
                make_field(reqId)]
    
            # send contract fields
            if self.serverVersion() >= MIN_SERVER_VER_TRADING_CLASS:
                flds += [make_field(contract.conId),]
            flds += [make_field(contract.symbol),
                make_field(contract.secType),
                make_field(contract.lastTradeDateOrContractMonth),
                make_field(contract.strike),
                make_field(contract.right),
                make_field(contract.multiplier),
                make_field(contract.exchange),
                make_field(contract.primaryExchange),
                make_field(contract.currency),
                make_field(contract.localSymbol)]
            if self.serverVersion() >= MIN_SERVER_VER_TRADING_CLASS:
                flds += [make_field(contract.tradingClass),]
            flds += [make_field(barSize),
                make_field(whatToShow),
                make_field(useRTH)]
    
            # send realTimeBarsOptions parameter
            if self.serverVersion() >= MIN_SERVER_VER_LINKING:
                realTimeBarsOptionsStr = ""
                if realTimeBarsOptions:
                    for tagValueOpt in realTimeBarsOptions:
                        realTimeBarsOptionsStr += str(tagValueOpt)
                flds += [make_field(realTimeBarsOptionsStr),]
    
            msg = "".join(flds)

        except ClientException as ex:
            self.wrapper.error(reqId, ex.code, ex.msg + ex.text)
            return
            
        self.sendMsg(msg)

        # TODO:
        #   get function name and log that into the database entry with the req id
        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id, symbol, security_type, exchange, currency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "reqRealTimeBars", OUT.REQ_REAL_TIME_BARS, contract.symbol, contract.secType, contract.exchange, contract.currency)
        )

    @overloaded
    def cancelRealTimeBars(self, reqId:TickerId):
        """Call the cancelRealTimeBars() function to stop receiving real time bar results.

        reqId:TickerId - The Id that was specified in the call to reqRealTimeBars(). """

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(reqId, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        VERSION = 1

        # send req mkt data msg
        flds = []
        flds += [make_field(OUT.CANCEL_REAL_TIME_BARS),
            make_field(VERSION),
            make_field(reqId)]

        msg = "".join(flds)
        self.sendMsg(msg)

        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id) VALUES (%s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "cancelTickByTickData", OUT.CANCEL_REAL_TIME_BARS)
        )

    @overloaded
    def reqAccountSummary(self, reqId:int, groupName:str, tags:str):
        """Call this method to request and keep up to date the data that appears
        on the TWS Account Window Summary tab. The data is returned by
        accountSummary().

        Note:   This request is designed for an FA managed account but can be
        used for any multi-account structure.

        reqId:int - The ID of the data request. Ensures that responses are matched
            to requests If several requests are in process.
        groupName:str - Set to All to returnrn account summary data for all
            accounts, or set to a specific Advisor Account Group name that has
            already been created in TWS Global Configuration.
        tags:str - A comma-separated list of account tags.  Available tags are:
            accountountType
            NetLiquidation,
            TotalCashValue - Total cash including futures pnl
            SettledCash - For cash accounts, this is the same as
            TotalCashValue
            AccruedCash - Net accrued interest
            BuyingPower - The maximum amount of marginable US stocks the
                account can buy
            EquityWithLoanValue - Cash + stocks + bonds + mutual funds
            PreviousDayEquityWithLoanValue,
            GrossPositionValue - The sum of the absolute value of all stock
                and equity option positions
            RegTEquity,
            RegTMargin,
            SMA - Special Memorandum Account
            InitMarginReq,
            MaintMarginReq,
            AvailableFunds,
            ExcessLiquidity,
            Cushion - Excess liquidity as a percentage of net liquidation value
            FullInitMarginReq,
            FullMaintMarginReq,
            FullAvailableFunds,
            FullExcessLiquidity,
            LookAheadNextChange - Time when look-ahead values take effect
            LookAheadInitMarginReq,
            LookAheadMaintMarginReq,
            LookAheadAvailableFunds,
            LookAheadExcessLiquidity,
            HighestSeverity - A measure of how close the account is to liquidation
            DayTradesRemaining - The Number of Open/Close trades a user
                could put on before Pattern Day Trading is detected. A value of "-1"
                means that the user can put on unlimited day trades.
            Leverage - GrossPositionValue / NetLiquidation
            $LEDGER - Single flag to relay all cash balance tags*, only in base
                currency.
            $LEDGER:CURRENCY - Single flag to relay all cash balance tags*, only in
                the specified currency.
            $LEDGER:ALL - Single flag to relay all cash balance tags* in all
            currencies."""

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        try:

            VERSION = 1

            msg = make_field(OUT.REQ_ACCOUNT_SUMMARY) \
               + make_field(VERSION)   \
               + make_field(reqId)     \
               + make_field(groupName) \
               + make_field(tags)

        except ClientException as ex:
            self.wrapper.error(reqId, ex.code, ex.msg + ex.text)
            return

        self.sendMsg(msg)

        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id) VALUES (%s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "reqAccountSummary", OUT.REQ_ACCOUNT_SUMMARY)
        )

    @overloaded
    def cancelAccountSummary(self, reqId:int):
        """Cancels the request for Account Window Summary tab data.

        reqId:int - The ID of the data request being canceled."""

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        VERSION = 1

        msg = make_field(OUT.CANCEL_ACCOUNT_SUMMARY) \
           + make_field(VERSION)   \
           + make_field(reqId)

        self.sendMsg(msg)

        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id) VALUES (%s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "cancelAccountSummary", OUT.CANCEL_ACCOUNT_SUMMARY)
        )

    @overloaded
    def reqPositions(self, reqId:int):
        """Requests real-time position data for all accounts."""

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        if self.serverVersion() < MIN_SERVER_VER_POSITIONS:
            self.wrapper.error(NO_VALID_ID, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                    "  It does not support positions request.")
            return

        VERSION = 1

        msg = make_field(OUT.REQ_POSITIONS) \
           + make_field(VERSION)

        self.sendMsg(msg)

        send_time = datetime.now().isoformat()
        self.db_conn.db_cur.execute(
            "INSERT INTO reqid_list (source, reqid, send_time, caller_func, caller_id) VALUES (%s, %s, %s, %s, %s)",
            ("ib_api", reqId, send_time, "reqAccountSummary", OUT.REQ_POSITIONS)
        )

    @overloaded
    def reqSecDefOptParams(self, reqId:int, underlyingSymbol:str,
                            futFopExchange:str, underlyingSecType:str,
                            underlyingConId:int):
        """Requests security definition option parameters for viewing a
        contract's option chain reqId the ID chosen for the request
        underlyingSymbol futFopExchange The exchange on which the returned
        options are trading. Can be set to the empty string "" for all
        exchanges. underlyingSecType The type of the underlying security,
        i.e. STK underlyingConId the contract ID of the underlying security.
        Response comes via EWrapper.securityDefinitionOptionParameter()"""

        self.logRequest(current_fn_name(), vars())

        if not self.isConnected():
            self.wrapper.error(NO_VALID_ID, NOT_CONNECTED.code(), NOT_CONNECTED.msg())
            return

        if self.serverVersion() < MIN_SERVER_VER_SEC_DEF_OPT_PARAMS_REQ:
            self.wrapper.error(NO_VALID_ID, UPDATE_TWS.code(), UPDATE_TWS.msg() +
                    "  It does not support security definition option request.")
            return

        try:
                
            flds = []
            flds += [make_field(OUT.REQ_SEC_DEF_OPT_PARAMS),
                make_field(reqId),
                make_field(underlyingSymbol),
                make_field(futFopExchange),
                make_field(underlyingSecType),
                make_field(underlyingConId)]
    
            msg = "".join(flds)
            
        except ClientException as ex:
            self.wrapper.error(reqId, ex.code, ex.msg + ex.text)
            return
            
        self.sendMsg(msg)