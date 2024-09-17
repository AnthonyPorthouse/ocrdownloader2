from abc import ABC, abstractmethod

from ..cli import Options
from ..data.track import Track


class Downloader(ABC):
    @abstractmethod
    def download(self, directory: str, track: Track, options: Options) -> None:
        pass  # pragma: no cover
