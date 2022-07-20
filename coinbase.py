from base64 import encode
import json
from client import Client
from json import loads
from datetime import datetime


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

        if 'sequence' in data:
            with self.lock:
                self.orderbook['bids'] = data['best_bid']
                self.orderbook['asks'] = data['best_ask']
                self.orderbook['price'] = data['price']
                self.orderbook['sequence'] = data['sequence']
                self.last_update['last_update'] = datetime.now()


        # Select the proper coin based on message type and pass the message to that object

        #testing output of result
        #print (data)


    # convert dict to string, subscribe to data streem by sending message
    def on_open(self, params):
        super().on_open()
        params = {
                    "type": "subscribe",
                    "product_ids": [
                        "ETH-USD"
                    ],
                    "channels": [
                        "level2_bulk", #toggle to level2 to get the full orderbook or level2_bulk to get aggregated feed
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
    