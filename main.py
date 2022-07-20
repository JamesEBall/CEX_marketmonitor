# -*- coding: utf-8 -*-

from coinbase import Coinbase
from datetime import datetime
from itertools import combinations 

import threading
import time


# calculate absolute delta in percentage
def delta(v1, v2):
    return abs((v2-v1)/v1)*100


# retrieve top bid/ask for each exchange
# calculate deltas
def calculate_price_delta(orderbooks, ex1, ex2):
    bid1 = float(orderbooks[ex1]['bids'][0][0])
    bid2 = float(orderbooks[ex2]['bids'][0][0])

    ask1 = float(orderbooks[ex1]['asks'][0][0])
    ask2 = float(orderbooks[ex2]['asks'][0][0])

    bid = delta(bid1, bid2)
    ask = delta(ask1, ask2)

    print(f'{ex1}-{ex2}\tBID Δ: {bid:.2f}% ASK Δ: {ask:.2f}%')

# return subsets of size 2 of all exchanges
def exchange_sets(orderbooks):
    exchanges = []

    # extract exchanges
    for exchange in orderbooks:
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
            if orderbooks['last_update'] != current_time:
                with lock:
                    # extract and print data
                    for exchanges in sets:
                        ex1, ex2 = exchanges
                        calculate_price_delta(orderbooks, ex1, ex2)
                    print(f"Last update: {orderbooks['last_update']}\n")

                    # set local last_update to last_update
                    current_time = orderbooks['last_update']
            time.sleep(0.1)
        except Exception:
            pass


if __name__ == "__main__":
    # data management
    lock = threading.Lock()
    orderbooks = {
        "Coinbase": {},
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