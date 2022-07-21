from base64 import encode
import json
from tokenize import Ignore
from tracemalloc import stop
from client import Client
from json import loads
from datetime import datetime
import csv


# inherits from Client
class Coinbase(Client):
    # call init from parent class
    def __init__(self, url, exchange, orderbook, lock):
        super().__init__(url, exchange)

        # local data management
        self.orderbook = orderbook['exchanges'][exchange]
        self.lock = lock
        self.last_update = orderbook

    def on_message(self, ws, message):

        data = json.loads(message)  # Load the JSON message sent

        # If the message is a snapshot, update the orderbook. If it did not recieve a snapshot, close.
        if ('type', 'snapshot') in data.items():
            with self.lock:
                #records snapshot of orderbook
                self.orderbook['type'] = data['type']
                self.orderbook['pair'] = data['product_id']
                self.orderbook['asks'] = data['asks'] #creates an orderbook from the snapshot.
                self.orderbook['bids'] = data['bids']
                self.orderbook['last_update'] = datetime.now()
                stop
        else:
            stop        # Select the proper coin based on message type and pass the message to that object




    # convert dict to string, subscribe to data streem by sending message
    def on_open(self, params):
        super().on_open()
        params = {
                    "type": "subscribe",
                    "product_ids": [
                        "ETH-USD"
                    ],
                    "channels": [
                        "level2", #toggle to level2 to get the full orderbook or level2_bulk to get aggregated feed
                        {
                            "name": "ticker",
                            "product_ids": [
                                "ETH-USD" #replace this with the product id of the coin you want to subscribe to
                            ]
                        }
                    ]
                }
        self.ws.send(json.dumps(params))

    def  on_close(self):   
        super().on_close()
        print("### closed ###")
    