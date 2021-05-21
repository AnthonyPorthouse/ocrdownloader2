import asyncio
import concurrent.futures
import os
import tempfile
from typing import IO, Set, Tuple

import requests

from .. import __user_agent__
from ..data.track import Track
from .downloader import Downloader

_headers = {"User-Agent": __user_agent__}


class PythonDownloader(Downloader):
    def download(self, directory: str, track: Track) -> None:
        file_size, filtered_mirrors = self._check_mirrors(track.links)

        chunk_size = file_size // len(filtered_mirrors)
        remainder = file_size % len(filtered_mirrors)

        downloads = []

        for i, mirror in enumerate(filtered_mirrors):
            start_pos = chunk_size * i
            to_pos = chunk_size * (i + 1) - 1

            if i == len(filtered_mirrors) - 1:
                to_pos += remainder + 1

            download = (i, mirror, start_pos, to_pos)

            downloads.append(download)

        """ @type Tuple[int, IO] results """
        results = asyncio.run(self._download(downloads))

        results.sort(key=lambda r: r[0])

        results = map(lambda r: r[1], results)

        filename = next(iter(track.links))

        with open(os.path.basename(filename), "wb") as output:
            for result in results:
                result.seek(0)
                output.write(result.read())
                result.close()

    @staticmethod
    def _check_mirrors(mirrors: Set[str]) -> Tuple[int, Set[str]]:
        file_size = None

        approved_mirrors = set()

        for mirror in mirrors:
            response = requests.head(mirror, headers=_headers)

            if file_size is None:
                file_size = int(response.headers.get("content-length"))

            if response.headers.get("accept-ranges") == "bytes":
                approved_mirrors.add(mirror)

        return file_size, approved_mirrors

    async def _download(self, downloads: list):

        loop = asyncio.get_running_loop()

        futures = []

        with concurrent.futures.ThreadPoolExecutor() as pool:
            for d in downloads:
                futures.append(
                    loop.run_in_executor(
                        pool, self._download_chunk, d[0], d[1], (d[2], d[3])
                    )
                )

            return await asyncio.gather(*futures)

    @staticmethod
    def _download_chunk(
        id: int, url: str, byte_range: Tuple[int, int]
    ) -> Tuple[int, IO]:
        file = tempfile.TemporaryFile()

        headers = _headers.copy()
        headers["range"] = f"bytes={byte_range[0]}-{byte_range[1]}"

        print(f"Starting chunk: {headers['range']}")
        response = requests.get(url, headers=headers, stream=True)
        file.write(response.content)

        print(f"Finishing chunk: {headers['range']}")

        return id, file
