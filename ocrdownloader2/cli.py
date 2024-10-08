import shutil
from typing import Optional

import click

from . import __version__
from .crawler import get_tracks
from .downloader import Engine, get_engine
from .downloaders.options import Options


@click.command()
@click.argument("start", type=click.IntRange(min=1, clamp=True))
@click.argument("end", type=click.IntRange(min=1, clamp=True), required=False)
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=True, file_okay=False, writable=True),
    default=".",
)
@click.option(
    "-p",
    "--python",
    is_flag=True,
    help="Force use of the python downloader, even if aria2 is available",
)
@click.option(
    "--no-checksum",
    is_flag=True,
    help="Don't check the validity of the file via the checksum",
)
@click.version_option(__version__)
def cli(
    start: int,
    end: Optional[int],
    output: str,
    python: bool = False,
    no_checksum: bool = False,
):
    """Parse and handle arguments to run OCR Downloader"""

    if end is None:
        end = start

    click.echo(_banner())
    click.echo()

    click.echo(f"From: {start}")
    click.echo(f"To: {end}")

    tracks = get_tracks(start, end)

    click.echo(f"Downloading to: {output}")

    engine = None

    if shutil.which("aria2c") is not None and not python:
        engine = Engine.ARIA_2

    engine = get_engine(engine)

    options = Options(use_python=python, use_checksum=not no_checksum)

    for track in tracks:
        click.echo(f"Downloading Track {track.id}")
        engine.download(output, track, options)


def _banner() -> str:
    """Return the banner as a string"""
    return "\n".join(
        [
            r"   ____  __________     ____                      __                __         ",
            r"  / __ \/ ____/ __ \   / __ \____ _      ______  / /___  ____  ____/ /__  _____",
            r" / / / / /   / /_/ /  / / / / __ \ | /| / / __ \/ / __ \/ __ \/ __  / _ \/ ___/",
            r"/ /_/ / /___/ _, _/  / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    ",
            r"\____/\____/_/ |_|  /_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/  2.0",
        ]
    )


if __name__ == "main":
    cli()
