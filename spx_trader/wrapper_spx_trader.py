import logging
import threading
import time
from datetime import datetime

from ibapi.common import * # @UnusedWildImport
from ibapi.utils import * # @UnusedWildImport
from ibapi.contract import (Contract, ContractDetails, DeltaNeutralContract)
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.execution import Execution
from ibapi.ticktype import * # @UnusedWildImport
from ibapi.commission_report import CommissionReport

from ibapi.wrapper import EWrapper

from common.ibcommon import overloaded
from database_spx_trader import spxTraderDBConn

logger = logging.getLogger(__name__)


class spxTraderWrapper(EWrapper):
    def __init__(self, db_conn:spxTraderDBConn):
        EWrapper.__init__(self)
        self.db_conn = db_conn
        self.verbose = False
        self.next_valid_id = None

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
        print("Next valid order ID: ", orderId)

        ### TODO
        self.next_valid_id = orderId

    @overloaded
    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""

        #TODO:
        # parse out the individual elements of the ContractDEtails object
        #    function that accesses the individual elements of the object and 
        #    displays them in a meaningful context
        self.logAnswer(current_fn_name(), vars())
        #print("Contract Details for reqID ", reqId)
        #print(contractDetails)
    
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

        if self.verbose is True:
            self.logAnswer(current_fn_name(), vars())
            print("<tickGeneric>",
                " Time recvd: ", datetime.now().isoformat(),
                " ReqId:", reqId,
                " tickType:", TickTypeEnum.idx2name[tickType],
                " value:", value
            )
        
        # self.db_conn.db_cur.execute(
        #     "INSERT INTO tick_generic (source, reqid, recv_time, field, name, value) VALUES (%s, %s, %s, %s, %s, %s)",
        #     ("ib_api", reqId, time_now, tickType, tick_name, value)
        # )

        insert_str = "INSERT INTO tick_generic (source, reqid, recv_time, field, name, value) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_var = ["ib_api", reqId, time_now, tickType, tick_name, value]
        self.db_conn.enqueue("tick_generic", insert_str, insert_var)

    @overloaded
    def tickPrice(self, reqId:TickerId , tickType:TickType, price:float,
                  attrib:TickAttrib):
        """Market data tick price callback. Handles all price related ticks."""
        time_now = datetime.now().isoformat()
        tick_name = TickTypeEnum.idx2name[tickType]

        if self.verbose is True:
            self.logAnswer(current_fn_name(), vars())
            print("<tickPrice>",
                " Time recvd:", time_now,
                " reqId:", reqId,
                " tickType:", tick_name,
                " price: ", price,
                " attrib:", attrib
            )

        # self.db_conn.db_cur.execute(
        #     "INSERT INTO tick_price (source, reqid, recv_time, field, name, price, attributes) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        #     ("ib_api", reqId, time_now, tickType, tick_name, price, str(attrib))
        # )

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
        
        # self.db_conn.db_cur.execute(
        #     "INSERT INTO tick_size (source, reqid, recv_time, field, name, size) VALUES (%s, %s, %s, %s, %s, %s)",
        #     ("ib_api", reqId, time_now, tickType, tick_name, size)
        # )

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
        
        # self.db_conn.db_cur.execute(
        #     "INSERT INTO tick_string (source, reqid, recv_time, field, name, string) VALUES (%s, %s, %s, %s, %s, %s)",
        #     ("ib_api", reqId, time_now, tickType, tick_name, value)
        # )

        insert_str= "INSERT INTO tick_string (source, reqid, recv_time, field, name, string) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_var= ["ib_api", reqId, time_now, tickType, tick_name, value]
        self.db_conn.enqueue("tick_string", insert_str, insert_var)

    @overloaded
    def tickReqParams(self, tickerId:int, minTick:float, bboExchange:str, snapshotPermissions:int):
        """returns exchange map of a particular contract"""
        self.logAnswer(current_fn_name(), vars())
        print("<tickReqParams>",
              " Time recvd: ", datetime.now().isoformat(),
              " reqId:", tickerId,
              " minTick:", minTick,
              " bboExchange:", bboExchange,
              ",snapshotPermissions:", snapshotPermissions)

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

        self.logAnswer(current_fn_name(), vars())

        print("RealTimeBar. TickerId:", reqId, time, open_, high, low, close, volume, wap, count)
        

    