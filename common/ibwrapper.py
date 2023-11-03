import logging

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

class ibWrapper(EWrapper):
    def __init__(self):
        EWrapper.__init__(self)

    # def logAnswer --- EWrapper method
        
    @overloaded
    def error(self, reqId:TickerId, errorCode:int, errorString:str, advancedOrderRejectJson = ""):
        """This event is called when there is an error with the
        communication or when TWS wants to send a message to the client."""

        if errorCode == -1:
            logger.info("info message from API %s %s %s", reqId, errorCode, errorString)
        else:
            self.logAnswer(current_fn_name(), vars())
            if advancedOrderRejectJson:
                logger.error("ERROR %s %s %s %s", reqId, errorCode, errorString, advancedOrderRejectJson)
            else: 
                logger.error("ERROR %s %s %s", reqId, errorCode, errorString)

    #def winError --- EWrapper method

    