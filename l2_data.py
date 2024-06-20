import logging
import time
import os
import psycopg

from ibapi.contract import Contract

from common.l2_ibclient import l2ibClient
from common.l2_ibwrapper import l2ibWrapper


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
    #logger.addHandler(console)


class l2ibTrader(l2ibClient, l2ibWrapper):
    def __init__(self):
        l2ibWrapper.__init__(self)
        l2ibClient.__init__(self, wrapper=self)
        self.db_conn = None

    def db_connection(self, config):
        try:
            self.db_conn = psycopg.connect(**config)
        except psycopg.Error as err:
            print(err)
            exit(1)

def main():
    SetupLogger()
    logger = logging.getLogger()
    #logger.info("INFO test logger message")

    l2_trader = l2ibTrader()

    db_config = {'user':'jeffrey',
                  'password':'strawberries',
                  'host':'127.0.0.1',
                  'port':'5432',
                  'dbname':'trader',
                  'autocommit':True} #this resolve the problem "InternalError: CREATE DATABASE cannot run inside a transaction block"
    
    l2_trader.db_connection(db_config)
    
    l2_trader.connect("127.0.0.1", 7496, clientId=1)
    
    con1 = Contract()
    con1.symbol = "NVDA"
    con1.secType = "STK"
    con1.exchange = "SMART"
    con1.currency = "USD"

    l2_trader.reqContractDetails(101, con1)
    time.sleep(.1)
    
    #trader.reqMktData(102, con1, '', False, False, '')
    #trader.reqTickByTickData(102, con1, 'AllLast', 0, False)
    l2_trader.reqMktDepth(103, con1, 20, True, [])
    
    key = input("Press \'q\' key to exit:")
    if key == "q":
        #client.file.close()
        l2_trader.disconnect()
        exit(0)



if __name__ == "__main__":
    main()