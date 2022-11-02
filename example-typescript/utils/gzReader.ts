const fs = require("fs");
const zlib = require("zlib");
const readline = require("readline");
function getUTCDateFromTime(date: any) {
  return date.toISOString().substring(0, 10);
}

export function getDay(startDate: string | number | Date) {
  return getUTCDateFromTime(new Date(startDate));
}

export class GzReader {
  unzip = zlib.createGunzip();
  fileContents: any;
  fileName: string;

  constructor(fileName: string) {
    this.fileName = fileName;
    console.log(`gunzip ${fileName}`);
    this.fileContents = fs.createReadStream(fileName);
  }

  async readStream(onData: (data: any) => any) {
    this.fileContents.on("pipe", (data: any) => {
      console.log("ReadStream: Piped on Stream...\n", data);
    });

    const streamReader = this.fileContents.pipe(this.unzip);
    let lineReader = readline.createInterface({
      input: streamReader,
    });
    streamReader.on(`error`, (err: any) => {
      console.error(`streamReader err ${this.fileName}`, err);
      fs.unlink(this.fileName, () => {});
    });
    lineReader.on("line", (line: string) => {
      onData(JSON.parse(line));
    });
    return new Promise((resolve, reject) => {
      this.fileContents.on("end", () => {
        console.log(`pipe finished`);
        resolve(this.fileName);
      });
    });
  }
}
