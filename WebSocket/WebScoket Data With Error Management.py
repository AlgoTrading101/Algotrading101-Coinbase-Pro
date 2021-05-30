import cbpro

wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com",
                                products=["ETH-USD", "BTC-USD"],
                                channels=["ticker"])

try:
    wsClient.start
except:
    print("Error")




