"""An interface to auto download market data"""

import logging
import os

from utils.common import ds_to_timestamp
from utils.dataloader import download_file
from utils.datareader import read_many_sources, DataSource

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    data_dir = "../data"
    filename = download_file(data_dir, "binance", "tf", "BTC_ETH", "2020-01-08")
    print(f"fdownload complete {filename}")
    # test read file
    for msg in read_many_sources(
            data_dir,
            sources=[
                DataSource("binance_fx", "obstream", "USD_BTC_perpetual_swap"),
                DataSource("binance_fx", "tf", "USD_BTC_perpetual_swap"),
            ],
            start_timestamp=ds_to_timestamp("2020-02-19") - 3600e3,
            end_timestamp=ds_to_timestamp("2020-02-19") + 3600e3,
        ):
            print("msg.ts", msg.ts)

# channel can be "tf" or "obstream"
