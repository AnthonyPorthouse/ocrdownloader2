import requests
import re
from typing import List, Optional
from bs4 import BeautifulSoup
from .track import Track

headers = {"User-Agent": "OCRDownloader/2.0.0"}


def get_tracks(start: int, end: int) -> List[Track]:
    tracks = []

    for track_id in range(start, end + 1):
        track = get_track(track_id)
        if track is None:
            continue

        tracks.append(track)

    return tracks


def backoff(func):
    from time import sleep

    sleep(2)

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@backoff
def get_track(track_id) -> Optional[Track]:

    print(f"Loading Track: {track_id}")

    url = get_url_for_track(track_id)

    try:
        with requests.get(url, headers=headers, timeout=2) as page:
            if page.status_code != 200:
                print("Not valid status code, skipping")
                return

            print("Parsing Page")

            soup = BeautifulSoup(page.content, "html5lib")
            modal = soup.find(id="modalDownload")

            checksum = re.search("MD5 Checksum: ([0-9a-f]{32})", modal.text).group(1)
            links = list(
                map(
                    lambda link: link["href"],
                    modal.find_all("a", href=re.compile("\\.mp3$")),
                )
            )

            return Track(id=track_id, checksum=checksum, links=links)
    except requests.exceptions.ConnectTimeout:
        print(f"Timed out connecting to {url}")

    return


def get_url_for_track(track_id) -> str:
    return "https://ocremix.org/remix/OCR{0:05d}".format(track_id)
