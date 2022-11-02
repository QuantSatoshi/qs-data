import datetime
from typing import Union

LOGGING_FORMAT = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"

def timestamp_to_dt(timestamp: Union[float, int]) -> datetime.datetime:
    """Convert a timestamp (milliseconds) to a UTC datetime object

    Args:
        timestamp (Union[float, int]): epoch timestamp in milliseconds

    Returns:
        datetime: A datetime object with tz set to the UTC timezone.
    """
    dt = datetime.datetime.fromtimestamp(timestamp / 1e3, tz=datetime.timezone.utc)
    return dt


def timestamp_to_ds(timestamp: Union[float, int]) -> str:
    """Convert a timestamp (millis) to a UTC date string

    Args:
        timestamp (Union[float, int]): epoch timestamp in milliseconds

    Returns:
        str: A date string (such as "2020-09-27") for the UTC timezone.
    """
    return timestamp_to_dt(timestamp).strftime("%Y-%m-%d")


def timestamp_to_ds_hms(timestamp: Union[float, int]) -> str:
    """Convert a timestamp (millis) to a UTC date string

    Args:
        timestamp (Union[float, int]): epoch timestamp in milliseconds

    Returns:
        str: A date string (such as "2020-09-27") for the UTC timezone.
    """
    return timestamp_to_dt(timestamp).strftime("%Y-%m-%d %H %M %S.%f")


def dt_to_timestamp(dt):
    timestamp_seconds = datetime.datetime.timestamp(
        dt.replace(tzinfo=datetime.timezone.utc)
    )
    return int(timestamp_seconds * 1e3)


def ds_to_timestamp(ds: str) -> int:
    """Convert a UTC date string to an epoch timestamp in milliseconds"""
    dt = datetime.datetime.strptime(ds, "%Y-%m-%d")  # dt has no timezone information
    timestamp_seconds = datetime.datetime.timestamp(
        dt.replace(tzinfo=datetime.timezone.utc)
    )
    return int(timestamp_seconds * 1e3)


def signal_time_str_to_timestamp(ds: str) -> int:
    """Convert a UTC date string to an epoch timestamp in milliseconds"""
    dt = datetime.datetime.strptime(
        ds, "%Y-%m-%d %H:%M:%S"
    )  # dt has no timezone information
    timestamp_seconds = datetime.datetime.timestamp(
        dt.replace(tzinfo=datetime.timezone.utc)
    )
    return int(timestamp_seconds * 1e3)


def book_time_str_to_timestamp(ds: str) -> int:
    """Convert a UTC date string to an epoch timestamp in milliseconds"""
    dt = datetime.datetime.strptime(
        ds, "%Y-%m-%dT%H:%M:%S.%fZ"
    )  # dt has no timezone information
    timestamp_seconds = datetime.datetime.timestamp(
        dt.replace(tzinfo=datetime.timezone.utc)
    )
    return int(timestamp_seconds * 1e3)


def signal_date_str_to_timestamp(ds: str) -> int:
    """Convert a UTC date string to an epoch timestamp in milliseconds"""
    dt = datetime.datetime.strptime(ds, "%Y-%m-%d")  # dt has no timezone information
    timestamp_seconds = datetime.datetime.timestamp(
        dt.replace(tzinfo=datetime.timezone.utc)
    )
    return int(timestamp_seconds * 1e3)
