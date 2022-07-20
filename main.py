# -*- coding: utf-8 -*-

from coinbase import Coinbase
from datetime import datetime
from itertools import combinations 

import threading
import time




# return subsets of size 2 of all exchanges
def exchange_sets(orderbooks):
    exchanges = []

    # extract exchanges
    for exchange in orderbooks['exchanges']:
        if exchange != 'last_update':
            exchanges.append(exchange)

    # return all subsets
    return list(combinations(exchanges, 2))

# print top bid/ask for each exchange
# run forever
def run(orderbooks, lock):
    # local last_update
    current_time = datetime.now()

    # exchange subsets
    sets = exchange_sets(orderbooks)

    while True:
        try:
            # check for new update
            if orderbooks['last_update'] != current_time and orderbooks['last_update'] != None:
                with lock:
                    # extract and print data
                    print(f"{'Exchange':<20} {'Bid':<10} {'Ask':<10} {'Price':<10}")
                    print(f"{'-'*20} {'-'*10} {'-'*10} {'-'*10}")
                    for exchange in orderbooks['exchanges']:
                        print(f"{str(exchange):<20} {orderbooks['exchanges'][exchange]['bids']:<10} {orderbooks['exchanges'][exchange]['asks']:<10} {orderbooks['exchanges'][exchange]['price']:<10}")
                    print(f"last update:", orderbooks['last_update'])
                    print(f"{'-'*53}")   
                    


                    # set local last_update to last_update
                    current_time = orderbooks['last_update']
            time.sleep(.05)
        except Exception:
            pass


if __name__ == "__main__":
    # data management
    lock = threading.Lock()
    orderbooks = {"exchanges": {"Coinbase": {}},
                    "last_update": None,
                }

    # create websocket threads
    coinbase = Coinbase(
        url="wss://ws-feed.exchange.coinbase.com",
        exchange="Coinbase",
        orderbook=orderbooks,
        lock=lock,
    )


    # start threads
    coinbase.start()

    # process websocket data
    run(orderbooks, lock)