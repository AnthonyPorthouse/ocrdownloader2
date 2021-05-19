import subprocess

from .. import __user_agent__
from ..data.track import Track
from .downloader import Downloader


class Aria2Downloader(Downloader):
    def download(self, directory: str, track: Track):
        command = [
            "aria2c",
            "--check-integrity=true",
            "--console-log-level=error",
            "--download-result=hide",
            f"--user-agent={__user_agent__}",
            f"--checksum=md5={track.checksum}",
            f"--dir={directory}",
        ]

        completed_process = subprocess.run(command + list(sorted(track.links)))

        if completed_process.returncode != 0:
            raise RuntimeError
