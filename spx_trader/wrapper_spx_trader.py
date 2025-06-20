import logging
import threading
import time
from datetime import datetime
import zmq

from ibapi.common import * 
from ibapi.utils import * 
from ibapi.server_versions import * 
from ibapi.contract import (Contract, ContractDetails, DeltaNeutralContract)
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.execution import Execution
from ibapi.ticktype import * 
from ibapi.commission_report import CommissionReport

from ibapi.wrapper import EWrapper

from common.ibcommon import overloaded
from database_spx_trader import spxTraderDBConn

logger = logging.getLogger(__name__)

# zmq ROUTER/DEALER pattern
# server is the ROUTER, client is the DEALER

    

# listening port for zmq messages
ZMQ_SERVER_PORT = 50000

# sendig port for zmq messages
ZMQ_CLIENT_PORT = 50001




class spxTraderWrapper(EWrapper):
    def __init__(self, db_conn:spxTraderDBConn):
        EWrapper.__init__(self)
        self.db_conn = db_conn
        self.verbose = False
        self.next_valid_id = None
        self.req_id_lock = threading.Lock()
        self.positions_event = threading.Event()
        self.positions_event.clear()
        self.wrapper_events = {}

        self.context = zmq.Context()
        self.zmq_server_socket = self.context.socket(zmq.REQ)
        self.zmq_client_socket = self.context.socket(zmq.REP)

    # def logAnswer --- EWrapper method
    # def db_conn_setup(self, config):
    #     self.db_conn = ibDBConn(config)

    @overloaded
    def error(self, reqId:TickerId, errorCode:int, errorString:str, advancedOrderRejectJson = ""):
        """This event is called when there is an error with the
        communication or when TWS wants to send a message to the client."""

        if errorCode == -1:
            logger.info("info message from API %s %s %s", reqId, errorCode, errorString)
            print("info message from API %s %s %s", reqId, errorCode, errorString)
        else:
            self.logAnswer(current_fn_name(), vars())
            if advancedOrderRejectJson:
                logger.error("ERROR %s %s %s %s", reqId, errorCode, errorString, advancedOrderRejectJson)
            else: 
                logger.error("ERROR %s %s %s", reqId, errorCode, errorString)
            if errorCode == 502:
                print("couldnt connect to TWS")

    #def winError --- EWrapper method
    
    @overloaded
    def nextValidId(self, orderId:int):
        """ Receives next valid order id."""

        self.logAnswer(current_fn_name(), vars())
        #print("from wrapper.nextValidId --- Next valid order ID: ", orderId)
        with self.req_id_lock:
            self.next_valid_id = orderId

    def get_req_id(self) -> int:
        """ Returns the next valid order ID."""
        with self.req_id_lock:
            if self.next_valid_id is None:
                return None
            else:
                current_id = self.next_valid_id   
                self.next_valid_id += 1
                return current_id

    @overloaded
    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""

        time_now = datetime.now().isoformat()

        #TODO:
        # parse out the individual elements of the ContractDEtails object
        #    function that accesses the individual elements of the object and 
        #    displays them in a meaningful context
        self.logAnswer(current_fn_name(), vars())
        #print("Contract Details for reqID ", reqId)
        #print(contractDetails)

        conid = contractDetails.contract.conId
        symbol = contractDetails.contract.symbol
        sec_type = contractDetails.contract.secType
        exchange = contractDetails.contract.exchange
        primary_exchange = contractDetails.contract.primaryExchange
        currency = contractDetails.contract.currency
        last_trade_date_or_contract_month = contractDetails.contract.lastTradeDateOrContractMonth
        strike = contractDetails.contract.strike
        right_ = contractDetails.contract.right
        trading_class = contractDetails.contract.tradingClass

        insert_str= "INSERT INTO tbt_all_last (source, reqid, recv_time, conid, symbol, sec_type, exchange, primary_exchange, currency, last_trade_date_or_contract_month, strike, right_, trading_class) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_var= ["ib_api", reqId, time_now, conid, symbol, sec_type, exchange, primary_exchange, currency, last_trade_date_or_contract_month, strike, right_, trading_class]
        self.db_conn.enqueue("contract", insert_str, insert_var)
        
    
    @overloaded
    def contractDetailsEnd(self, reqId:int):
        """This function is called once all contract details for a given
        request are received. This helps to define the end of an option
        chain."""

        #TODO:
        # experiment with an options chain (?) to see if handling this function
        #    call is necessary
        self.logAnswer(current_fn_name(), vars())
        #print("ContractDetailsEnd for reqid ", reqId)

        

    @overloaded
    def updateMktDepth(self, reqId:TickerId , position:int, operation:int,
                        side:int, price:float, size:Decimal):
        """Returns the order book.

        tickerId -  the request's identifier
        position -  the order book's row being updated
        operation - how to refresh the row:
            0 = insert (insert this new order into the row identified by 'position')
            1 = update (update the existing order in the row identified by 'position')
            2 = delete (delete the existing order at the row identified by 'position').
        side -  0 for ask, 1 for bid
        price - the order's price
        size -  the order's size"""

        self.logAnswer(current_fn_name(), vars())
        pass

    @overloaded
    def updateMktDepthL2(self, reqId:TickerId , position:int, marketMaker:str,
                          operation:int, side:int, price:float, size:Decimal, isSmartDepth:bool):
        """Returns the order book.

        tickerId -  the request's identifier
        position -  the order book's row being updated
        marketMaker - the exchange holding the order
        operation - how to refresh the row:
            0 = insert (insert this new order into the row identified by 'position')
            1 = update (update the existing order in the row identified by 'position')
            2 = delete (delete the existing order at the row identified by 'position').
        side -  0 for ask, 1 for bid
        price - the order's price
        size -  the order's size
        isSmartDepth - is SMART Depth request"""

        self.logAnswer(current_fn_name(), vars())
        pass

    @overloaded
    def tickGeneric(self, reqId:TickerId, tickType:TickType, value:float):
        time_now = datetime.now().isoformat()
        tick_name = TickTypeEnum.idx2name[tickType]

        # if self.verbose is True:
        #     self.logAnswer(current_fn_name(), vars())
        #     print("<tickGeneric>",
        #         " Time recvd: ", datetime.now().isoformat(),
        #         " ReqId:", reqId,
        #         " tickType:", TickTypeEnum.idx2name[tickType],
        #         " value:", value
        #     )

        insert_str = "INSERT INTO tick_generic (source, reqid, recv_time, field, name, value) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_var = ["ib_api", reqId, time_now, tickType, tick_name, value]
        self.db_conn.enqueue("tick_generic", insert_str, insert_var)

    @overloaded
    def tickPrice(self, reqId:TickerId , tickType:TickType, price:float,
                  attrib:TickAttrib):
        """Market data tick price callback. Handles all price related ticks."""
        time_now = datetime.now().isoformat()
        tick_name = TickTypeEnum.idx2name[tickType]

        # if self.verbose is True:
        #     self.logAnswer(current_fn_name(), vars())
        #     print("<tickPrice>",
        #         " Time recvd:", time_now,
        #         " reqId:", reqId,
        #         " tickType:", tick_name,
        #         " price: ", price,
        #         " attrib:", attrib
        #     )

        insert_str = "INSERT INTO tick_price (source, reqid, recv_time, field, name, price, attributes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        insert_var = ["ib_api", reqId, time_now, tickType, tick_name, price, str(attrib)]
        self.db_conn.enqueue("tick_price", insert_str, insert_var)

    @overloaded
    def tickSize(self, reqId:TickerId, tickType:TickType, size:Decimal):
        """Market data tick size callback. Handles all size-related ticks."""
        time_now = datetime.now().isoformat()
        tick_name = TickTypeEnum.idx2name[tickType]

        # if self.verbose is True:
        #     self.logAnswer(current_fn_name(), vars())
        #     print("<tickSize>",
        #             " Time recvd: ", time_now,
        #             " reqId:", reqId,
        #             " tickType", tick_name,
        #             " size:", size
        #     )

        insert_str = "INSERT INTO tick_size (source, reqid, recv_time, field, name, size) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_var = ["ib_api", reqId, time_now, tickType, tick_name, size]
        self.db_conn.enqueue("tick_size", insert_str, insert_var)
        
    @overloaded
    def tickString(self, reqId:TickerId, tickType:TickType, value:str):
        time_now = datetime.now().isoformat()
        tick_name = TickTypeEnum.idx2name[tickType]

        # if self.verbose is True:
        #     self.logAnswer(current_fn_name(), vars())
        #     print("<tickString>",
        #         " Time recvd: ", datetime.now().isoformat(),
        #         " reqId:", reqId,
        #         " tickType", TickTypeEnum.idx2name[tickType],
        #         " str: ", value
        #     )

        insert_str= "INSERT INTO tick_string (source, reqid, recv_time, field, name, string) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_var= ["ib_api", reqId, time_now, tickType, tick_name, value]
        self.db_conn.enqueue("tick_string", insert_str, insert_var)

    @overloaded
    # this seems to be called when calling contract details?
    def tickReqParams(self, tickerId:int, minTick:float, bboExchange:str, snapshotPermissions:int):
        """returns exchange map of a particular contract"""
        self.logAnswer(current_fn_name(), vars())
        # print("<tickReqParams>",
        #       " Time recvd: ", datetime.now().isoformat(),
        #       " reqId:", tickerId,
        #       " minTick:", minTick,
        #       " bboExchange:", bboExchange,
        #       ",snapshotPermissions:", snapshotPermissions)

    @overloaded
    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: Decimal, tickAttribLast: TickAttribLast, exchange: str,
                          specialConditions: str):
        """returns tick-by-tick data for tickType = "Last" or "AllLast" """
        
        time_now = datetime.now().isoformat()
        if tickType == 0:
            tick_name = "Last"
        elif tickType == 1:
            tick_name = "AllLast"
        else:
            tick_name = "Unknown"
        
        # if self.verbose is True:
        #     self.logAnswer(current_fn_name(), vars())
        #     print("<tickByTickAllLast>",
        #       " Time recvd:", datetime.now().isoformat(), 
        #       " ReqId:", reqId, 
        #       " tickType:", TickTypeEnum.idx2name[tickType], 
        #       " Time:", time,
        #       " Price:", floatMaxString(price), 
        #       " Size:", size,
        #       " Exch:" , exchange,
        #       " Spec Cond:", specialConditions, 
        #       " PastLimit:", tickAttribLast.pastLimit,
        #       " Unreported:", tickAttribLast.unreported
        #     )
        
        # self.db_conn.db_cur.execute(
        #     "INSERT INTO tbt_all_last (source, reqid, recv_time, tick_type, tick_name, ib_time, price, size, exchange, spec_cond, past_limit, unreported) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        #     ("ib_api", reqId, time_now, tickType, tick_name, time, price, size, exchange, specialConditions, tickAttribLast.pastLimit, tickAttribLast.unreported)
        # )

        insert_str= "INSERT INTO tbt_all_last (source, reqid, recv_time, tick_type, tick_name, ib_time, price, size, exchange, spec_cond, past_limit, unreported) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_var= ["ib_api", reqId, time_now, tickType, tick_name, time, price, size, exchange, specialConditions, tickAttribLast.pastLimit, tickAttribLast.unreported]
        self.db_conn.enqueue("tbt_all_last", insert_str, insert_var)

    @overloaded
    def historicalTicks(self, reqId: int, ticks: ListOfHistoricalTick, done: bool):
        """returns historical tick data when whatToShow=MIDPOINT"""
        #self.logAnswer(current_fn_name(), vars())
        pass

    @overloaded
    def historicalTicksBidAsk(self, reqId: int, ticks: ListOfHistoricalTickBidAsk, done: bool):
        """returns historical tick data when whatToShow=BID_ASK"""
        #self.logAnswer(current_fn_name(), vars())
        pass

    @overloaded
    def historicalTicksLast(self, reqId: int, ticks: ListOfHistoricalTickLast, done: bool):
        """returns historical tick data when whatToShow=TRADES"""
        #self.logAnswer(current_fn_name(), vars())
        pass

    @overloaded
    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: Decimal, askSize: Decimal, tickAttribBidAsk: TickAttribBidAsk):
        """returns tick-by-tick data for tickType = "BidAsk" """
        #self.logAnswer(current_fn_name(), vars())
        pass

    @overloaded
    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        """returns tick-by-tick data for tickType = "MidPoint" """
        #self.logAnswer(current_fn_name(), vars())
        pass

    @overloaded
    def realtimeBar(self, reqId: TickerId, time:int, open_: float, high: float, low: float, close: float,
                        volume: Decimal, wap: Decimal, count: int):

        """ Updates the real time 5 seconds bars

        reqId - the request's identifier
        bar.time  - start of bar in unix (or 'epoch') time
        bar.endTime - for synthetic bars, the end time (requires TWS v964). Otherwise -1.
        bar.open_  - the bar's open value
        bar.high  - the bar's high value
        bar.low   - the bar's low value
        bar.close - the bar's closing value
        bar.volume - the bar's traded volume if available
        bar.WAP   - the bar's Weighted Average Price
        bar.count - the number of trades during the bar's timespan (only available
            for TRADES)."""

        time_now = datetime.now().isoformat()

        self.logAnswer(current_fn_name(), vars())
        #print("RealTimeBar. TickerId:", reqId, time, open_, high, low, close, volume, wap, count)

        insert_str = "INSERT INTO rtb (source, reqid, recv_time, bar_time, bar_open_, bar_high, bar_low, bar_close, bar_volume, bar_wap, bar_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_var = ["ib_api", reqId, time_now, time, open_, high, low, close, volume, wap, count]
        self.db_conn.enqueue("rtb", insert_str, insert_var) 

    def accountSummary(self, reqId:int, account:str, tag:str, value:str,
                       currency:str):
        """Returns the data from the TWS Account Window Summary tab in
        response to reqAccountSummary()."""

        self.logAnswer(current_fn_name(), vars())    
        print("Account: ", account, " Tag: ", tag, " Value: ", value, " Currency: ", currency)

    @overloaded
    def position(self, account:str, contract:Contract, position:Decimal,
                 avgCost:float):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""
        
        # whenever a posistion is being updated, unset the event
        self.positions_event.clear()
        time_now = datetime.now().isoformat()

        self.logAnswer(current_fn_name(), vars())
        #print("Position.", "Account:", account, "Symbol:", contract.symbol, "opt exp:", contract.lastTradeDateOrContractMonth, "ConId:", contract.conId, "SecType:", contract.secType,
        #      "Currency:", contract.currency, "Position:", position, "Avg cost:", avgCost)
        
        insert_str = "INSERT INTO positions (source, recv_time, account, position, avg_cost, symbol, sec_type, last_trade_date_or_contract_month, strike, type, multiplier, sec_id_type, sec_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_var = ["ib_api", time_now, account, position, avgCost, contract.symbol, contract.secType, contract.lastTradeDateOrContractMonth, contract.strike, contract.right, contract.multiplier, contract.secIdType, contract.secId, contract.description]
        self.db_conn.enqueue("positions", insert_str, insert_var) 

    def positionEnd(self):
        """This is called once all position data for a given request are
        received and functions as an end marker for the position() data. """

        self.logAnswer(current_fn_name(), vars())
        print("")
        print("----PositionEnd---------------------")    
        print("")

        # when the posistions are done updating, set the event
        self.positions_event.set()

    def securityDefinitionOptionParameter(self, reqId:int, exchange:str,
        underlyingConId:int, tradingClass:str, multiplier:str,
        expirations:SetOfString, strikes:SetOfFloat):
        """ Returns the option chain for an underlying on an exchange
        specified in reqSecDefOptParams There will be multiple callbacks to
        securityDefinitionOptionParameter if multiple exchanges are specified
        in reqSecDefOptParams

        reqId - ID of the request initiating the callback
        underlyingConId - The conID of the underlying security
        tradingClass -  the option trading class
        multiplier -    the option multiplier
        expirations - a list of the expiries for the options of this underlying
             on this exchange
        strikes - a list of the possible strikes for options of this underlying
             on this exchange """

        self.logAnswer(current_fn_name(), vars())


    def securityDefinitionOptionParameterEnd(self, reqId:int):
        """ Called when all callbacks to securityDefinitionOptionParameter are
        complete

        reqId - the ID used in the call to securityDefinitionOptionParameter """

        self.logAnswer(current_fn_name(), vars())


    