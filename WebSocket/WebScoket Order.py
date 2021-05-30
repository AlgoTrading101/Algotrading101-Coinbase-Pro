import cbpro
import base64
import json
from time import sleep

key = ''
secret = ''
passphrase = ''

encoded = json.dumps(secret).encode()
b64secret = base64.b64encode(encoded)
auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)
c = cbpro.PublicClient()

class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["BTC-USDT"]
        self.channels=["ticker"]
        self.ticker = 0

    def on_message(self, msg):
        if 'price' in msg and 'type' in msg:
            print ("Tracker:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))
            self.ticker = float(msg['price'])

    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()

try:
    wsClient.start()
except:
    print("Unable to connect")

print(wsClient.url, wsClient.products)
while (wsClient.ticker < 33500.00):
    sleep(1)

print(wsClient.ticker)
try:
    wsClient.close()
except:
    print("Unable to close socket")

try:
    limit = c.get_product_ticker(product_id='ETH-USDT')
except Exception as e:
    print('Error obtaining ticker data')
        
try:
    order=auth_client.place_limit_order(product_id='ETH-USDT', 
                        side='buy', 
                        price=float(limit['price'])+2, 
                        size='0.007')
except Exception as e:
    print('Error placing order')
        
sleep(2)
        
try:
    check = order['id']
    check_order = auth_client.get_order(order_id=check)
except Exception as e:
    print('Unable to check order. It might be rejected.')
        
if check_order['status'] == 'done':
    print('Order placed successfully')
    print(check_order)
else:
    print('Order was not matched')
