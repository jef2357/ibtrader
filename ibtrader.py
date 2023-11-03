import logging
import time
import os

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
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)


class ibTrader(ibClient, ibWrapper):
    def __init__(self):
        ibWrapper.__init__(self)
        ibClient.__init__(self, wrapper=self)

def main():
    SetupLogger()

    logger = logging.getLogger()
    logger.info("INFO test logger message")

    trader = ibTrader()

    trader.connect("127.0.0.1", 7496, clientId=1)

    #trader.run()

    # key = input("Press \'c\' to continue:")
    # if key == 'c':
    
    # AMD ------------------------------------------------------------------------
    con1 = Contract()
    con1.symbol = "AMD"
    con1.secType = "STK"
    con1.exchange = "SMART"
    con1.currency = "USD"

    #trader.reqContractDetails(101, con1)
    time.sleep(1)
    #trader.reqMatchingSymbols(102,"INTC")
    #time.sleep(1)
    #trader.reqMktData(103, con1, '', False, False, '')
    #trader.reqTickByTickData(400, con1, 'AllLast', 0, False)
    trader.reqMktDepth(1002, con1, 100, True, '')

    #trader.reqMatchingSymbols(1000,"SPX")

    # con2 = Contract()
    # con2.symbol = "SPXESUP"
    # con2.secType = "IND"
    # con2.exchange = "CME"
    # con2.currency = "USD"

    #trader.reqContractDetails(101, con2)
    #time.sleep(1)
    #trader.reqTickByTickData(1001, con2, 'AllLast', 0, False)

    #trader.disconnect()
    #exit(0)

    # SPX ------------------------------------------------------------------------
    # con3 = Contract()
    # con3.symbol = "SPX"
    # con3.secType = "IND"
    # con3.exchange = "CBOE"
    # con3.currency = "USD"
    # #trader.reqContractDetails(3000, con3)
    # time.sleep(1)
    # #trader.reqTickByTickData(3001, con3, 'AllLast', 0, False)
    # trader.reqMktData(3002, con3, '', False, False, '')


    key = input("Press \'q\' key to exit:")
    if key == "q":
        #client.file.close()
        trader.disconnect()
        exit(0)



if __name__ == "__main__":
    main()