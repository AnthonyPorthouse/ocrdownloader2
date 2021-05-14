import subprocess

from .track import Track


def download(directory: str, track: Track):
    print(f"Downloading Track {track.id}")
    aria2_download(directory, track)


def aria2_download(directory: str, track: Track):
    command = [
        "aria2c",
        "--quiet",
        "--check-integrity=true",
        f"--checksum=md5={track.checksum}",
        f"--dir={directory}",
    ]

    subprocess.run(command + track.links)
