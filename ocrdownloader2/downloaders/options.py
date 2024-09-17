from dataclasses import dataclass


@dataclass
class Options:
    use_python: bool = False
    use_checksum: bool = True
