from .. import __user_agent__
from .downloader import Downloader
from ..data.track import Track
import subprocess


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

        completed_process = subprocess.run(command + list(track.links))

        if completed_process.returncode != 0:
            raise RuntimeError
