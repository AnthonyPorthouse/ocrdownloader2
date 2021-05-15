from abc import ABC, abstractmethod

from ..data.track import Track


class Downloader(ABC):
    @abstractmethod
    def download(self, directory: str, track: Track):
        pass
