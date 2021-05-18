import pytest

from ocrdownloader2.downloader import get_engine
from ocrdownloader2.downloaders.downloader import Downloader


@pytest.mark.parametrize("engine", ["aria2", None])
def test_get_engine(engine):
    engine = get_engine()
    assert isinstance(engine, Downloader)
