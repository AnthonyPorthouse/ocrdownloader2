import requests
import re
from typing import List, Optional, Tuple, Set
from bs4 import BeautifulSoup, Tag
from . import __user_agent__
from .data.track import Track
from .data.author import Author

headers = {"User-Agent": __user_agent__}


def get_tracks(start: int, end: int) -> List[Track]:
    tracks = []

    for track_id in range(start, end + 1):
        track = get_track(track_id)
        if track is None:
            continue

        print(f"Track: {track.title}")
        print(f"Authors: {', '.join(map(lambda author : author.name, track.authors))}")

        tracks.append(track)

    return tracks


def _backoff(func):
    from time import sleep

    sleep(2)

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@_backoff
def get_track(track_id) -> Optional[Track]:

    print(f"Loading Track: {track_id}")

    url = _get_url_for_track(track_id)

    try:
        with requests.get(url, headers=headers, timeout=2) as page:
            if page.status_code != 200:
                print("Not valid status code, skipping")
                return

            print("Parsing Page")

            page = BeautifulSoup(page.content, "html5lib")

            checksum, links = _get_track_info(page)
            authors = _get_track_authors(page)
            title = _get_track_title(page)

            return Track(
                id=track_id,
                title=title,
                authors=authors,
                checksum=checksum,
                links=links,
            )
    except requests.exceptions.ConnectTimeout:
        print(f"Timed out connecting to {url}")

    return


def _get_url_for_track(track_id) -> str:
    return "https://ocremix.org/remix/OCR{0:05d}".format(track_id)


def _get_track_info(page: BeautifulSoup) -> Tuple[str, Set[str]]:
    modal = page.find(id="modalDownload")

    checksum = re.search("MD5 Checksum: ([0-9a-f]{32})", modal.text).group(1)
    links = set(
        map(
            lambda link: link["href"],
            modal.find_all("a", href=re.compile("\\.mp3$")),
        )
    )

    return checksum, links


def _get_track_authors(page: BeautifulSoup) -> List[Author]:
    byline = page.find("h2")
    raw_authors = byline.find_all("a", href=True)

    def get_author_from_element(element: Tag) -> Author:
        return Author(name=element.string, url=element["href"])

    return list(map(get_author_from_element, raw_authors))


def _get_track_title(page: BeautifulSoup) -> str:
    return page.find("meta", property="og:title")["content"].removesuffix(" OC ReMix")
