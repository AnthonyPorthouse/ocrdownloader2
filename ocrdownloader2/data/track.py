from dataclasses import dataclass
from typing import List, Set

from .author import Author


@dataclass
class Track:
    id: int
    title: str
    checksum: str
    links: Set[str]
    authors: List[Author]
