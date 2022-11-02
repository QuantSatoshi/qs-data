"""An interface to auto download market data"""

import logging
import os

import requests


logger = logging.getLogger(__name__)

def download_file(data_dir:str, exchange: str, channel: str, pair: str, date_str: str):
    # first, let's check if the file exists in local data folder
    pathprefix = filename = os.path.join(data_dir, f"{channel}/{exchange}")
    accessKey = os.getenv('ACCESS_KEY')
    if not accessKey:
        raise Exception("require ACCESS_KEY env var")
    filename = os.path.join(pathprefix, f"{channel}-{exchange}-{pair}-{date_str}.gz")
    if os.path.exists(filename):
        logger.info(f"file exists {filename}")
        return filename

    if not os.path.exists(pathprefix):
        os.makedirs(pathprefix)

    # if data doesn't exist, download
    download_prefix = "http://data.quantsatoshi.com/api/download-data"

    url = f"{download_prefix}?channel={channel}&exchange={exchange}&pair={pair}&startDate={date_str}&accessKey={accessKey}"
    print(f"downloading data {url}")
    try:
        r = requests.get(url, allow_redirects=True, timeout=None)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
                logger.info(f"downloaded {filename}")
                return filename
        else:
            logger.info(
                f"file download failed {filename}"
            )
            raise Exception(f"downloading failed {r.status_code} {r.text}")
    except Exception as e:
        logger.warning(f"Failed to download from {url}: {e}")
