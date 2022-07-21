# -*- coding: utf-8 -*-

from coinbase import Coinbase
from datetime import datetime
from itertools import combinations 

import threading
import time

import pandas as pd



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
            
            with lock:
                for exchange in orderbooks['exchanges']:
                    pd.DataFrame.from_dict((orderbooks['exchanges'][exchange]['asks'])).to_csv(f'{exchange} asks.csv')
                    pd.DataFrame.from_dict((orderbooks['exchanges'][exchange]['bids'])).to_csv(f'{exchange} bids.csv')
                    print(f'{exchange} data written to file')
            break
        except Exception:
            pass
        time.sleep(1)

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
    # Code executed here
    run(orderbooks, lock)
    