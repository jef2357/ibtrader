from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, Market
from typing import List, Union
from datetime import datetime

c = WebSocketClient(api_key='yr0XKLtp8UBRdlHUWYJK85d6iaqlNDI3',feed='delayed.polygon.io',market='stocks',subscriptions=["T.TSLA"])

def handle_msg(msgs: List[WebSocketMessage]):
    for m in msgs:
        time = datetime.fromtimestamp(m.timestamp/1000)
        print(time.isoformat('_',timespec='milliseconds'), '    ', m.symbol, f"{m.size:9}", f"{m.price:9.4f}")

def main():
    c.run(handle_msg)

main()