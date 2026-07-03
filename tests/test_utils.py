from datetime import datetime

import pytest

from waybackpy import __version__
from waybackpy.utils import DEFAULT_USER_AGENT, parse_wayback_datetime


def test_default_user_agent() -> None:
    assert (
        DEFAULT_USER_AGENT
        == f"waybackpy {__version__} - https://github.com/akamhy/waybackpy"
    )


def test_parse_wayback_datetime_14_digits() -> None:
    """Standard 14‑digit Wayback timestamp parses as‑is."""
    ts = "20220102130405"
    dt = parse_wayback_datetime(ts)
    assert dt == datetime(2022, 1, 2, 13, 4, 5)


def test_parse_wayback_datetime_12_digits() -> None:
    """
    12‑digit timestamps (YYYYMMDDhhmm) are accepted and seconds are assumed 00.
    """
    ts = "202201021304"
    dt = parse_wayback_datetime(ts)
    assert dt == datetime(2022, 1, 2, 13, 4, 0)


def test_parse_wayback_datetime_normalizes_zero_day() -> None:
    """
    Timestamps with day '00' are normalized to day 1.
    Example from the docstring: '20000900190155' -> 2000‑09‑01 19:01:55.
    """
    ts = "20000900190155"
    dt = parse_wayback_datetime(ts)
    assert dt == datetime(2000, 9, 1, 19, 1, 55)


def test_parse_wayback_datetime_normalizes_invalid_day_and_month() -> None:
    """
    Out‑of‑range month and day values are clamped into valid ranges.
    """
    # Month 13 -> 12, day 32 -> last day of month (31 for December 2024)
    ts = "20241332000000"
    dt = parse_wayback_datetime(ts)
    assert dt == datetime(2024, 12, 31, 0, 0, 0)

    # February 30 2024 -> February 29 2024 (leap year)
    ts_feb = "20240230000000"
    dt_feb = parse_wayback_datetime(ts_feb)
    assert dt_feb == datetime(2024, 2, 29, 0, 0, 0)


def test_parse_wayback_datetime_clamps_time_components() -> None:
    """Hours/minutes/seconds are clamped into valid ranges."""
    ts = "20220101199999"  # 19 -> 19, 99 -> 59, 99 -> 59
    dt = parse_wayback_datetime(ts)
    assert dt == datetime(2022, 1, 1, 19, 59, 59)


@pytest.mark.parametrize(
    "ts",
    [
        "",
        "abc",
        "2022-01-01",
        "1234567890123",  # 13 digits, neither 12 nor 14
        "123456789012345",  # 15 digits
    ],
)
def test_parse_wayback_datetime_invalid_input_raises(ts: str) -> None:
    """Non‑conforming strings should raise ValueError."""
    with pytest.raises(ValueError):
        parse_wayback_datetime(ts)
