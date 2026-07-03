"""
Utility functions and shared variables like DEFAULT_USER_AGENT are here.
"""

from datetime import datetime
import calendar
import re

from . import __version__

DEFAULT_USER_AGENT: str = (
    f"waybackpy {__version__} - https://github.com/akamhy/waybackpy"
)


def unix_timestamp_to_wayback_timestamp(unix_timestamp: int) -> str:
    """
    Converts Unix time to Wayback Machine timestamp, Wayback Machine
    timestamp format is yyyyMMddhhmmss.
    """
    return datetime.utcfromtimestamp(int(unix_timestamp)).strftime("%Y%m%d%H%M%S")


def wayback_timestamp(**kwargs: int) -> str:
    """
    Prepends zero before the year, month, day, hour and minute so that they
    are conformable with the YYYYMMDDhhmmss Wayback Machine timestamp format.
    """
    return "".join(
        str(kwargs[key]).zfill(2) for key in ["year", "month", "day", "hour", "minute"]
    )


def parse_wayback_datetime(ts: str) -> datetime:
    """
    Parse a Wayback timestamp robustly.
    Accepts 14 digits (YYYYMMDDhhmmss) or 12 digits (YYYYMMDDhhmm),
    normalizes '00' month/day etc. to valid calendar values.

    Examples:
      '20000900190155' -> 2000-09-01 19:01:55   (day 00 -> 01)
    """
    ts = ts.strip()

    # Allow 12-digit timestamps by assuming seconds=00
    if re.fullmatch(r"\d{12}", ts):
        ts = ts + "00"
    if not re.fullmatch(r"\d{14}", ts):
        raise ValueError(f"Invalid Wayback timestamp: '{ts}'")

    y = int(ts[0:4])
    m = int(ts[4:6])
    d = int(ts[6:8])
    H = int(ts[8:10])
    M = int(ts[10:12])
    S = int(ts[12:14])

    # Normalize out-of-range values (notably 00 for month/day)
    m = 1 if m == 0 else min(max(m, 1), 12)
    last_day = calendar.monthrange(y, m)[1]
    d = 1 if d == 0 else min(max(d, 1), last_day)
    H = min(max(H, 0), 23)
    M = min(max(M, 0), 59)
    S = min(max(S, 0), 59)

    return datetime(y, m, d, H, M, S)
