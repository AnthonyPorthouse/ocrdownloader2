from abc import ABC, abstractmethod

from ..data.track import Track
from .options import Options


class Downloader(ABC):
    @abstractmethod
    def download(self, directory: str, track: Track, options: Options) -> None:
        pass  # pragma: no cover
