import { getDay, GzReader } from "./utils/gzReader";
const fs = require("fs");
const mkdirp = require("mkdirp");
import axios from "axios";
const dataPrefix = __dirname + `/../../data`;

async function downloadOne(
  startDate: string,
  channel: string,
  exchange: string,
  pair: string
) {
  const accessKey = process.env.ACCESS_KEY;
  if (!accessKey) {
    throw new Error(`accessKey is missing`);
  }

  const utcDateHour = getDay(startDate);
  const outputFileName = `${channel}/${exchange}/${channel}-${exchange}-${pair}-${utcDateHour}.gz`;
  await mkdirp(dataPrefix + "/" + `${channel}/${exchange}`);
  const outputFileFullPath = dataPrefix + "/" + outputFileName;
  if (fs.existsSync(outputFileFullPath)) {
    console.log(`skip downloading existing file ${outputFileName}`);
    return outputFileFullPath;
  }
  const url = `http://data.quantsatoshi.com/api/download-data`;

  console.log(`start downloading file ${outputFileName}`);
  try {
    const response = await axios({
      url,
      params: { exchange, pair, startDate, channel, accessKey },
      method: "GET",
      responseType: "stream",
    });
    const writer = fs.createWriteStream(outputFileFullPath);
    return new Promise((resolve, reject) => {
      response.data.pipe(writer);
      let error: any = null;
      writer.on("error", (err: any) => {
        error = err;
        writer.close();
        reject(err);
      });
      writer.on("close", () => {
        if (!error) {
          console.log(`download complete`, outputFileFullPath);
          resolve(outputFileFullPath);
        }
      });
    });
  } catch (e: any) {
    if (e.response.status !== 200) {
      console.error(`got error ${e.response.status} ${e.response.data}`);
      return;
    }
  }
}

export async function readLocalDataFile(fileName: string, onDataRow: (row: any) => any) {
  const reader = new GzReader(`${fileName}`);
  await reader.readStream(data => {
    return onDataRow(data);
  });
}

async function main() {
  const channel = "tf"; // can be obstream, tf, tick
  const exchange = "binance"; // can be binance, gdax, bybit
  const pair = "USDT_BTC";
  const startTs = new Date("2021-06-27T00:00:00.000Z").getTime();
  const endTs = new Date("2021-06-28T00:00:00.000Z").getTime();
  for (let ts = startTs; ts < endTs; ts += 86400000) {
    const startDate = new Date(ts).toISOString();
    console.log(`startDate`, startDate);
    const filename = await downloadOne(startDate, channel, exchange, pair);
    if (filename) {
      await readLocalDataFile(filename as string, (row: any) => {
        // Do something with the data
        console.log(row);
      });
    }
  }
  process.exit(0);
}

main();

// tsc && node --max-old-space-size=16000  dist/entry/downloadFile.js
