import click
from typing import Optional
from .crawler import get_tracks
from .downloader import download


@click.command()
@click.argument("start", type=click.IntRange(min=1, clamp=True))
@click.argument("end", type=click.IntRange(min=1, clamp=True), required=False)
def cli(start: int, end: Optional[int]):
    """Parse and handle arguments to run OCR Downloader"""

    if end is None:
        end = start

    click.echo(banner())
    click.echo()

    click.echo(f"From: {start}")
    click.echo(f"To: {end}")

    tracks = get_tracks(start, end)

    for track in tracks:
        download(track)


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
