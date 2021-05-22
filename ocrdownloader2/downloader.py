from enum import Enum
from typing import Optional

from .downloaders.aria2_downloader import Aria2Downloader
from .downloaders.python_downloader import PythonDownloader


class Engine(Enum):
    ARIA_2 = "aria2"
    PYTHON = "python"


engines = {
    Engine.ARIA_2: lambda: Aria2Downloader(),
    Engine.PYTHON: lambda: PythonDownloader(),
}


def get_engine(engine: Optional[Engine] = None):
    if engine is None:
        engine = Engine.PYTHON

    return engines[engine]()
