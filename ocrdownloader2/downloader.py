from enum import Enum
from typing import Optional

from .downloaders.aria2_downloader import Aria2Downloader


class Engine(Enum):
    ARIA_2 = "aria2"


engines = {
    Engine.ARIA_2: lambda: Aria2Downloader(),
}


def get_engine(engine: Optional[Engine] = None):
    if engine is None:
        engine = Engine.ARIA_2

    return engines[engine]()
