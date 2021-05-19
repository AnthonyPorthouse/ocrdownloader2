from ocrdownloader2 import __user_agent__
from ocrdownloader2.data.track import Track
from ocrdownloader2.downloaders.aria2_downloader import Aria2Downloader


def test_download(fake_process):
    fake_process.register_subprocess(
        [
            "aria2c",
            "--check-integrity=true",
            "--console-log-level=error",
            "--download-result=hide",
            f"--user-agent={__user_agent__}",
            f"--checksum=md5=123abc",
            f"--dir=directory",
            "1",
            "2",
        ]
    )

    downloader = Aria2Downloader()
    downloader.download(
        "directory",
        Track(id=1, title="test", authors=[], links={"1", "2"}, checksum="123abc"),
    )

    assert fake_process.call_count(["aria2c", fake_process.any()]) == 1
