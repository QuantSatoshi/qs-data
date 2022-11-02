"""An interface to read market data"""

__all__ = ["DataSource", "read_many_sources", "MessageEntry"]

import datetime
import gzip
import json
import logging
import os
from dataclasses import dataclass
from heapq import heapify, heappop, heapreplace
from typing import Any, Iterator, List

from utils.dataloader import download_file
from utils.common import ds_to_timestamp, timestamp_to_ds, timestamp_to_dt

logger = logging.getLogger(__name__)


def read_data2(filename: str):
    try:
        logger.info(f"Reading from {filename}")
        with gzip.open(filename, mode="rt") as f:
            for row in f:
                if "bybit" in filename and row[0] != "[" and row[0] != "{":
                    print("skip row", row)
                    continue
                parsed = json.loads(row.rstrip("\n"))
                if "merged" in parsed:
                    yield from parsed["merged"]
                else:
                    yield parsed
    except Exception as e:
        # delete the file due to the file is probably corrupted
        logger.warning(f"Failed to read from {filename}: {e}")
        os.remove(filename)
        logger.warning(f"deleted corrupted file: {filename}")


def parse_msg_timestamp(msg) -> int:
    """Parse timestamp (millis) from message"""

    if isinstance(msg, list):
        if isinstance(msg[0], int):
            # print("using raw[0] ts 2", msg)
            return msg[0]
        elif "ts" in msg[0]:
            if isinstance(msg[0]["ts"], str):
                return int(
                    datetime.datetime.timestamp(
                        datetime.datetime.strptime(
                            msg[0]["ts"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        )
                    )
                    * 1000
                )
            else:
                # print("using raw[0] ts", msg[0]["ts"])
                return msg[0]["ts"]
    elif isinstance(msg, dict) and "ts" in msg:
        if isinstance(msg["ts"], str):
            return int(
                datetime.datetime.timestamp(
                    datetime.datetime.strptime(msg["ts"], "%Y-%m-%dT%H:%M:%S.%f%z")
                )
                * 1000
            )
        else:
            # print("using raw ts", msg["ts"])
            return msg["ts"]
    else:
        raise ValueError(msg)


CHANNELS = ["obstream", "tf", "liquidations", "candle_300", "candle_60"]

@dataclass(frozen=True)
class DataSource:
    exchange: str = "bitmex_fx"
    channel: str = "obstream"
    symbol: str = "USD_BTC_perpetual_swap"

    def __post_init__(self):
        if self.channel not in CHANNELS:
            raise ValueError(self.channel)


def read_one_source(
    data_dir: str,
    source: DataSource,
    start_timestamp: float,
    end_timestamp: float,
):
    ts_day_start = int(ds_to_timestamp(timestamp_to_ds(start_timestamp)))
    last_ts = None
    while ts_day_start < end_timestamp:
        ds = timestamp_to_ds(ts_day_start)
        ts_day_end = ts_day_start + 86400 * 1000
        filename = os.path.join(
            data_dir,
            f"{source.channel}/{source.exchange}/{source.channel}-{source.exchange}-{source.symbol}-{ds}.gz",
        )
        download_file(data_dir, source.exchange, source.channel, source.symbol, ds)
        for idx, msg in enumerate(read_data2(filename)):
            if (
                source.exchange == "binance_fx"
                and source.channel == "obstream"
                and msg.get("e") == "s"
            ):
                # ignore all snapshots for binance data
                # because their timestamp is often out of order
                continue
            # if (msg[0]!='['):
            #    continue
            current_ts = parse_msg_timestamp(msg)
            if current_ts < ts_day_start or current_ts > ts_day_end:
                logger.warn(
                    f"Found corrupted data in file: {filename}. "
                    f"Row {idx} has timestamp {current_ts} ({timestamp_to_dt(current_ts)}), "
                    f"which is not in the expected range between {ts_day_start} and {ts_day_end}."
                )
                continue
            if last_ts is not None and last_ts > current_ts:  # give some buffer ms
                if msg.get("action") == "partial" or msg.get("e") == "s":
                    # partial update messages are often out of order, and we just silently ignore them
                    continue
                event_name = msg.get("e")
                message = (
                    f"Found corrupted data in file: {filename}. "
                    f"Row {idx} e={event_name} has timestamp {current_ts} ({timestamp_to_dt(current_ts)}), "
                    f"which is smaller than previous timestamp {last_ts} ({timestamp_to_dt(last_ts)})."
                )
                logger.warning(message)
                continue
                # raise Exception(message)
            if current_ts > end_timestamp:
                return
            elif current_ts >= start_timestamp:
                yield current_ts, msg
                last_ts = current_ts
        ts_day_start += 86400 * 1000


@dataclass
class MessageEntry:
    ts: int
    message: Any
    source: DataSource


def read_many_sources(
    data_dir: str,
    sources: List[DataSource],
    start_timestamp: float,
    end_timestamp: float,
) -> Iterator[MessageEntry]:
    cache = [None] * len(sources)
    entries = []  # Heap of [ts, idx, iterator].
    for idx, source in enumerate(sources):
        it = iter(
            read_one_source(
                data_dir,
                source=source,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
            )
        )
        try:
            ts, msg = next(it)
        except StopIteration:
            break
        entries.append([ts, idx, it])
        cache[idx] = MessageEntry(ts, msg, source)
    heapify(entries)
    while entries:
        ts, idx, it = entry = entries[0]
        yield cache[idx]
        try:
            cache[idx].ts, cache[idx].message = next(it)
            entry[0] = cache[idx].ts
            heapreplace(entries, entry)
        except StopIteration:
            heappop(entries)
