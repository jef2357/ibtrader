import logging
import time
import os
import psycopg
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ibapi.contract import Contract
    
from client_spx_trader import spxTraderClient
from wrapper_spx_trader import spxTraderWrapper
from database_spx_trader import spxTraderDBConn

from spx_trader_main_window import spxTraderMainWindow
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtCore import Qt, QAbstractTableModel

def SetupLogger(log_level):
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=log_level,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(log_level)
    #logger.addHandler(console)
    
class spxTrader(spxTraderClient, spxTraderWrapper):
    def __init__(self, db_config):
        self.db_conn = spxTraderDBConn(db_config)
        spxTraderWrapper.__init__(self, self.db_conn)
        spxTraderClient.__init__(self, self, self.db_conn)


def main():
    log_level = logging.WARNING
    #SetupLogger(log_level)
    #logger = logging.getLogger()
    #logger.info("INFO test logger message")
    db_config = {'user':'jeffrey',
                 'password':'strawberries',
                 'host':'127.0.0.1',
                 'port':'5432',
                 'dbname':'trader_today',
                 'autocommit':True} #this resolve the problem "InternalError: CREATE DATABASE cannot run inside a transaction block"

    app = QApplication(sys.argv)
    trader = spxTrader(db_config)
    spx_trader = spxTraderMainWindow(trader)
    spx_trader.show()

    app.exec()
    # this line is causing the app to not exit after closing all windows
    #sys.exit(app.exec())


if __name__ == "__main__":
    main()