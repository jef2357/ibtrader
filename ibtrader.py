import logging
import time
import os
import psycopg

from ibapi.contract import Contract

from common.ibclient import ibClient
from common.ibwrapper import ibWrapper


def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.WARNING,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    #logger.addHandler(console)


class ibTrader(ibClient, ibWrapper):
    def __init__(self):
        ibWrapper.__init__(self)
        ibClient.__init__(self, wrapper=self)


def main():
    SetupLogger()
    logger = logging.getLogger()
    #logger.info("INFO test logger message")
    
    print("creating ibtrader object")
    trader = ibTrader()

    db_config = {'user':'jeffrey',
                  'password':'strawberries',
                  'host':'127.0.0.1',
                  'port':'5432',
                  'dbname':'trader',
                  'autocommit':True} #this resolve the problem "InternalError: CREATE DATABASE cannot run inside a transaction block"
    
    trader.wrapper_db_setup(db_config)
    trader.client_db_setup(db_config)

    print("connecting to ibapi")
    trader.connect("127.0.0.1", 7496, clientId=1)

    #trader.reqIds(0)

    # AMD ------------------clear
    # ------------------------------------------------------
    # TODO:
    #   use reqContractDetails to get contract object from the api
    # SPX ------------------------------------------------------------------------
    contract_spx = Contract()
    contract_spx.symbol = "SPX"
    contract_spx.secType = "IND"
    contract_spx.exchange = "CBOE"
    contract_spx.currency = "USD"
    trader.reqContractDetails(101, contract_spx)
    trader.reqMktData(103, contract_spx, '', False, False, '')
    
    contract_AMD = Contract()
    contract_AMD.symbol = "AMD"
    contract_AMD.secType = "STK"
    contract_AMD.exchange = "SMART"
    contract_AMD.currency = "USD"
    trader.reqContractDetails(201, contract_AMD)
    trader.reqMktData(202, contract_AMD, '', False, False, '')
    trader.reqTickByTickData(203, contract_AMD, 'AllLast', 0, False)
    #trader.reqMktDepth(404, con3, 10, True, [])
    #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_NVDA = Contract()
    contract_NVDA.symbol = "NVDA"
    contract_NVDA.secType = "STK"
    contract_NVDA.exchange = "SMART"
    contract_NVDA.currency = "USD"
    trader.reqContractDetails(301, contract_NVDA)
    trader.reqMktData(302, contract_NVDA, '', False, False, '')
    trader.reqTickByTickData(303, contract_NVDA, 'Last', 0, False)
    #trader.reqMktDepth(404, con3, 10, True, [])
    #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_MSFT = Contract()
    contract_MSFT.symbol = "MSFT"
    contract_MSFT.secType = "STK"
    contract_MSFT.exchange = "SMART"
    contract_MSFT.currency = "USD"
    trader.reqContractDetails(401, contract_MSFT)
    trader.reqMktData(402, contract_MSFT, '', False, False, '')
    trader.reqTickByTickData(403, contract_MSFT, 'AllLast', 0, False)
    # #trader.reqMktDepth(404, con3, 10, True, [])
    # #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_NFLX = Contract()
    contract_NFLX.symbol = "NFLX"
    contract_NFLX.secType = "STK"
    contract_NFLX.exchange = "SMART"
    contract_NFLX.currency = "USD"
    trader.reqContractDetails(501, contract_NFLX)
    trader.reqMktData(502, contract_NFLX, '', False, False, '')
    trader.reqTickByTickData(503, contract_NFLX, 'AllLast', 0, False)
    # #trader.reqMktDepth(404, con3, 10, True, [])
    # #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_TSM = Contract()
    contract_TSM.symbol = "TSM"
    contract_TSM.secType = "STK"
    contract_TSM.exchange = "SMART"
    contract_TSM.currency = "USD"
    trader.reqContractDetails(601, contract_TSM)
    trader.reqMktData(602, contract_TSM, '', False, False, '')
    #trader.reqTickByTickData(603, contract_TSM, 'AllLast', 0, False)
    # #trader.reqMktDepth(404, con3, 10, True, [])
    # #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_AMZN = Contract()
    contract_AMZN.symbol = "AMZN"
    contract_AMZN.secType = "STK"
    contract_AMZN.exchange = "SMART"
    contract_AMZN.currency = "USD"
    trader.reqContractDetails(701, contract_AMZN)
    trader.reqMktData(702, contract_AMZN, '', False, False, '')
    #trader.reqTickByTickData(703, contract_AMZN, 'AllLast', 0, False)
    #trader.reqMktDepth(404, con3, 10, True, [])
    #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_DELL = Contract()
    contract_DELL.symbol = "DELL"
    contract_DELL.secType = "STK"
    contract_DELL.exchange = "SMART"
    contract_DELL.currency = "USD"
    trader.reqContractDetails(801, contract_DELL)
    trader.reqMktData(802, contract_DELL, '', False, False, '')
    #trader.reqTickByTickData(803, contract_DELL, 'AllLast', 0, False)
    #trader.reqMktDepth(404, con3, 10, True, [])
    #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_INTC = Contract()
    contract_INTC.symbol = "INTC"
    contract_INTC.secType = "STK"
    contract_INTC.exchange = "SMART"
    contract_INTC.currency = "USD"
    trader.reqContractDetails(901, contract_INTC)
    trader.reqMktData(902, contract_INTC, '', False, False, '')
    #trader.reqTickByTickData(903, contract_INTC, 'AllLast', 0, False)
    #trader.reqMktDepth(404, con3, 10, True, [])
    #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_MU = Contract()
    contract_MU.symbol = "MU"
    contract_MU.secType = "STK"
    contract_MU.exchange = "SMART"
    contract_MU.currency = "USD"
    trader.reqContractDetails(1001, contract_MU)
    trader.reqMktData(1002, contract_MU, '', False, False, '')
    #trader.reqTickByTickData(1003, contract_MU, 'AllLast', 0, False)
    #trader.reqMktDepth(404, con3, 10, True, [])
    #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_WDC = Contract()
    contract_WDC.symbol = "WDC"
    contract_WDC.secType = "STK"
    contract_WDC.exchange = "SMART"
    contract_WDC.currency = "USD"
    trader.reqContractDetails(1101, contract_WDC)
    trader.reqMktData(1102, contract_WDC, '', False, False, '')
    #trader.reqTickByTickData(1103, contract_WDC, 'AllLast', 0, False)
    #trader.reqMktDepth(404, con3, 10, True, [])
    #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])

    contract_AVGO = Contract()
    contract_AVGO.symbol = "AVGO"
    contract_AVGO.secType = "STK"
    contract_AVGO.exchange = "SMART"
    contract_AVGO.currency = "USD"
    trader.reqContractDetails(1201, contract_AVGO)
    trader.reqMktData(1202, contract_AVGO, '', False, False, '')
    trader.reqTickByTickData(1203, contract_AVGO, 'AllLast', 0, False)
    #trader.reqMktDepth(404, con3, 10, True, [])
    #trader.reqRealTimeBars(405, con3, 5, "TRADES", True, [])


    key = input("Press \'q\' key to exit:")
    if key == "q":
        #client.file.close()
        trader.disconnect()
        exit(0)


if __name__ == "__main__":
    main()