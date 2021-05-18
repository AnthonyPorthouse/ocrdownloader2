import pytest
import os.path

import requests
from bs4 import BeautifulSoup

from ocrdownloader2.crawler import (
    get_tracks,
    get_track,
    _get_url_for_track,
    _get_track_title,
)


@pytest.mark.parametrize(
    "track_id, expected",
    [
        (0, "https://ocremix.org/remix/OCR00000"),
        ("1", "https://ocremix.org/remix/OCR00001"),
        (22.0, "https://ocremix.org/remix/OCR00022"),
        (99999, "https://ocremix.org/remix/OCR9999"),
        (100000, "https://ocremix.org/remix/OCR100000"),
    ],
)
def test_url_generation(track_id, expected: str):
    url = _get_url_for_track(0)
    assert url == "https://ocremix.org/remix/OCR00000"


def test_get_track(requests_mock):
    with open(os.path.dirname(__file__) + "/data/page_response.html") as body:
        requests_mock.get("https://ocremix.org/remix/OCR00000", text=body.read())

    track = get_track(0)

    assert track.id == 0
    assert track.title == 'The Legend of Zelda: Breath of the Wild "Torchlight"'
    assert track.checksum == "5753dc3e406eaf3d23887299961a14bc"
    assert track.links == {
        "https://iterations.org/files/music/remixes/Legend_of_Zelda_Breath_of_the_Wild_Torchlight_OC_ReMix.mp3",
        "https://ocrmirror.org/files/music/remixes/Legend_of_Zelda_Breath_of_the_Wild_Torchlight_OC_ReMix.mp3",
        "https://ocr.blueblue.fr/files/music/remixes/Legend_of_Zelda_Breath_of_the_Wild_Torchlight_OC_ReMix.mp3",
    }


def test_get_track_with_missing_page(requests_mock):
    requests_mock.get("https://ocremix.org/remix/OCR00000", status_code=404)

    track = get_track(0)

    assert track is None


def test_get_track_with_timeout(requests_mock):
    requests_mock.get(
        "https://ocremix.org/remix/OCR00000", exc=requests.exceptions.ConnectTimeout
    )

    track = get_track(0)

    assert track is None


def test_get_tracks(requests_mock):
    with open(os.path.dirname(__file__) + "/data/page_response.html") as body:
        requests_mock.get("https://ocremix.org/remix/OCR00000", text=body.read())

    tracks = get_tracks(0, 0)

    assert len(tracks) == 1


def test_get_tracks_with_bad_responses(requests_mock):
    with open(os.path.dirname(__file__) + "/data/page_response.html") as body:
        requests_mock.get("https://ocremix.org/remix/OCR00000", status_code=404)
        requests_mock.get("https://ocremix.org/remix/OCR00001", text=body.read())

    tracks = get_tracks(0, 1)

    assert len(tracks) == 1
    assert tracks[0].id == 1


def test_get_track_title():
    data = r"""<!DOCTYPE html>
    <html><head>
    <meta property="og:title" content='The Legend of Zelda: Breath of the Wild "Torchlight" OC ReMix'>
    </head>
    <body>
    </body>
    </html>
    """

    elements = BeautifulSoup(data, "html5lib")
    assert (
        _get_track_title(elements)
        == 'The Legend of Zelda: Breath of the Wild "Torchlight"'
    )
