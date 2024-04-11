
## download raw qs data
```
url is http://data.quantsatoshi.com/api/download-data?exchange=binance&pair=BUSD_BTC&startDate=2022-02-04&channel=tf&accessKey=[your access key]
```
```
channel: 
  - tf  (trades)
  - obstream (orderbook stream)
  - ticker
  - candle300 (5 mins candle)
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
