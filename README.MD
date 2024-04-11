
## download raw qs data
```
url is http://data.quantsatoshi.com/api/download-data?exchange=binance&pair=BUSD_BTC&startDate=2022-02-04&channel=tf&accessKey=[your access key]
```
```
channel: 
  - tf  (trades)
  - obstream (orderbook stream)
  - ticker
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
