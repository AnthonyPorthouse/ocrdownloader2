from dataclasses import dataclass
from typing import List


@dataclass
class Track:
    id: int
    checksum: str
    links: List[str]
