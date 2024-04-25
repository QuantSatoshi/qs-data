
## download raw qs data
```
url is http://data.quantsatoshi.com/api/download-data?exchange=binance&pair=BUSD_BTC&startDate=2022-02-04&channel=tf&accessKey=[your access key]
```
```
channel: 
  - tf  (trades)
  - obstream (orderbook stream)
  - tick
  - candle_300 (5 mins candle)
```

## using typescript
```
cd example-typescript
npm run tsc
ACCESS_KEY=[your access key] node --max-old-space-size=16000 dist/entry/downloadFile.js
```

## using python 3
```
cd example-python
pip install requests
ACCESS_KEY=[your access key] python downloadFile.py 
```
## list of exchanges
```
"binance",
"binance_coin",
"binance_fx",
"binance_fx_coin",
"bitfinex",
"bitmex_fx",
"bitstamp",
"bittrex",
"bybit",
"bybit_fx",
"coinbase_fx",
"coinsbit",
"deribit",
"dgax",
"fatbtc",
"gdax",
"hbdm_fx",
"huobi",
"huobi_fx",
"itbit",
"loopring",
"okcoin_fx",
"okex_spot",
"okex_swap_fx",
"phemex"
```

## list of pairs per exchange
```
curl http://data.300k.xyz/data-api/get-pairs/tf/binance
```

## list dates for exchange
```
curl http://data.300k.xyz/data-api/get-data-dates/tf/binance/USDT_ETH
curl http://data.300k.xyz/data-api/get-data-dates/candle_300/binance_fx/USD_ETH_perpetual_swap
```

## data format

```
channel=tf  trades
[1713228662938,0,63187.5,0.002,304,1713228662634]
timestamp received, side, price, amount, pairCode(ignore), timestamp event
side: 1: taker is buy, 0: taker is sell
```

```
channel=obstream
{"ts":1711584656072,"e":"u","c":304,"b":[[1000,205.208],[5000,0.531]],"a":[[69748.5,0.138]]}
ts: timestamp received
e: u for update, s for snapshot
b: bids [[price, amount]]
a: asks [[price, amount]]
```

```
channel=candle_300
[1688168700000,30474.5,30512.3,30470,30501,205.84300000000022,223.68500000000088,6277673.762699998,6822090.013800003]
[timestamp, open, high, low, close, buy_volume, sell_volume, buy_cost, sell_cost]
```

```
channel=tick
[1700877413994,37796,37796.1,3.514,3.292]
[timestamp, bid_price, ask_price, bid_amount, ask_amount]
```

