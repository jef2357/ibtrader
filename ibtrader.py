import logging
import time
import os

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
                        level=logging.DEBUG,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
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

    trader.run()


if __name__ == "__main__":
    main()