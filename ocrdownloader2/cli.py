import click
from typing import Optional
from .crawler import get_tracks
from .downloader import get_engine
from . import __version__


@click.command()
@click.argument("start", type=click.IntRange(min=1, clamp=True))
@click.argument("end", type=click.IntRange(min=1, clamp=True), required=False)
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=True, file_okay=False, writable=True),
    default=".",
)
@click.version_option(__version__)
def cli(start: int, end: Optional[int], output: str):
    """Parse and handle arguments to run OCR Downloader"""

    if end is None:
        end = start

    click.echo(banner())
    click.echo()

    click.echo(f"From: {start}")
    click.echo(f"To: {end}")

    tracks = get_tracks(start, end)

    click.echo(f"Downloading to: {output}")

    engine = get_engine()

    for track in tracks:
        click.echo(f"Downloading Track {track.id}")
        engine.download(output, track)


def banner() -> str:
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
