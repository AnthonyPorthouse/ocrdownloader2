import re

from ocrdownloader2 import __version__


def test_version():
    assert isinstance(__version__, str)
    assert re.match(r"\d+\.\d+\.\d+", __version__)
