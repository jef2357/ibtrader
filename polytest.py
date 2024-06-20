
# From the polygon help chat:
# from polygon import WebSocketClient
# from polygon.websocket.models import WebSocketMessage, Market
# from typing import List, Union

# c = WebSocketClient(api_key='yr0XKLtp8UBRdlHUWYJK85d6iaqlNDI3',feed='delayed.polygon.io',market='stocks',subscriptions=["Q.TSLA"])
# def handle_msg(msgs: List[WebSocketMessage]):
#     for m in msgs: print(m)

# def main(): c.run(handle_msg)

# main()

# docs
# https://polygon.io/docs/stocks/ws_stocks_am
# https://polygon-api-client.readthedocs.io/en/latest/WebSocket.html#


from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, Market
from typing import List
from datetime import datetime
import time

#client = WebSocketClient(api_key='yr0XKLtp8UBRdlHUWYJK85d6iaqlNDI3', market=Market.Indices,feed='delayed.polygon.io')

stock_client = WebSocketClient(api_key='yr0XKLtp8UBRdlHUWYJK85d6iaqlNDI3', market=Market.Stocks,feed='delayed.polygon.io')
index_client = WebSocketClient(api_key='yr0XKLtp8UBRdlHUWYJK85d6iaqlNDI3', market=Market.Indices,feed='delayed.polygon.io')


#stock_client.subscribe("T.AAPL") # multiple tickers
# stock_client.subscribe("T.MSFT") # multiple tickers
# stock_client.subscribe("T.AMZN") # multiple tickers
stock_client.subscribe("T.NVDA") # multiple tickers
# stock_client.subscribe("T.GOOGL") # multiple tickers
# stock_client.subscribe("T.TSLA") # multiple tickers
# stock_client.subscribe("T.META") # multiple tickers
# stock_client.subscribe("T.GOOG") # multiple tickers
#client.subscribe("T.BRK.B") # multiple tickers
#stock_client.subscribe("T.UNH") # multiple tickers

#index_client.subscribe("AM.I:SPX")  # Standard & Poor's 500
index_client.subscribe("V.I:SPX") # Standard & Poor's 500


def handle_msg_stock(msgs: List[WebSocketMessage]):
    for m in msgs:
        #print(m.symbol, m.price, m.size, m.timestamp, m.sequence_number, m.id)

        #utc_time = time.gmtime(m.timestamp/1000)
        #local_time = time.localtime(m.timestamp/1000)

        time = datetime.fromtimestamp(m.timestamp/1000)

        #print(time.strftime("%Y-%m-%d %H:%M:%S", local_time)) 
        #print(time.strftime("%Y-%m-%d %H:%M:%S.%f", local_time),m.symbol, m.size, m.price)
        #print(time.isoformat('_',timespec='milliseconds'), m.symbol, m.size, m.price)

        print(time.isoformat('_',timespec='milliseconds'), '    ', m.symbol, "{:9.0f}".format(m.size), "{:9.4f}".format(m.price))

def handle_msg_index(msgs: List[WebSocketMessage]):
    for m in msgs:
        #print(m.symbol, m.price, m.size, m.timestamp, m.sequence_number, m.id)

        #utc_time = time.gmtime(m.timestamp/1000)
        #local_time = time.localtime(m.timestamp/1000)

        time = datetime.fromtimestamp(m.timestamp/1000)

        #print(time.strftime("%Y-%m-%d %H:%M:%S", local_time)) 
        #print(time.strftime("%Y-%m-%d %H:%M:%S.%f", local_time),m.symbol, m.size, m.price)
        #print(time.isoformat('_',timespec='milliseconds'), m.symbol, m.size, m.price)

        #print(time.isoformat('_',timespec='milliseconds'), '    ', m.symbol, "{:9.0f}".format(m.size), "{:9.4f}".format(m.price))

        print(time.isoformat('_',timespec='milliseconds'), '    ', f"{m.ticker:9}", f"{m.value:9.3f}")

def main():
    #stock_client.run(handle_msg)
    #index_client.run(handle_msg_index)
    stock_client.run(handle_msg_stock)

main()