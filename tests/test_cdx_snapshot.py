from datetime import datetime
from typing import Dict

from waybackpy.cdx_snapshot import CDXSnapshot


def test_CDXSnapshot() -> None:
    sample_input = (
        "org,archive)/ 20080126045828 http://github.com "
        "text/html 200 Q4YULN754FHV2U6Q5JUT6Q2P57WEWNNY 1415"
    )
    prop_values = sample_input.split(" ")
    properties = {}
    (
        properties["urlkey"],
        properties["timestamp"],
        properties["original"],
        properties["mimetype"],
        properties["statuscode"],
        properties["digest"],
        properties["length"],
    ) = prop_values

    snapshot = CDXSnapshot(properties)

    assert properties["urlkey"] == snapshot.urlkey
    assert properties["timestamp"] == snapshot.timestamp
    assert properties["original"] == snapshot.original
    assert properties["mimetype"] == snapshot.mimetype
    assert properties["statuscode"] == snapshot.statuscode
    assert properties["digest"] == snapshot.digest
    assert properties["length"] == snapshot.length
    assert (
        datetime.strptime(properties["timestamp"], "%Y%m%d%H%M%S")
        == snapshot.datetime_timestamp
    )
    archive_url = (
        "https://web.archive.org/web/"
        + properties["timestamp"]
        + "/"
        + properties["original"]
    )
    assert archive_url == snapshot.archive_url
    assert sample_input == str(snapshot)
    assert sample_input == repr(snapshot)

def test_CDXSnapshot_with_non_standard_timestamp() -> None:
    """
    CDXSnapshot should use parse_wayback_datetime and cope with timestamps
    that need normalization (e.g. day '00').
    """
    sample_input = (
        "org,archive)/ 20000900190155 http://github.com "
        "text/html 200 Q4YULN754FHV2U6Q5JUT6Q2P57WEWNNY 1415"
    )
    prop_values = sample_input.split(" ")
    properties: Dict[str, str] = {}
    (
        properties["urlkey"],
        properties["timestamp"],
        properties["original"],
        properties["mimetype"],
        properties["statuscode"],
        properties["digest"],
        properties["length"],
    ) = prop_values

    snapshot = CDXSnapshot(properties)
    assert snapshot.datetime_timestamp == datetime(2000, 9, 1, 19, 1, 55)
    assert snapshot.timestamp == "20000900190155"
