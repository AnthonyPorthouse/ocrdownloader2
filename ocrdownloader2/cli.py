import click

from .crawler import get_tracks
from .downloader import download


@click.command()
@click.argument("from", type=click.IntRange(min=1, clamp=True))
@click.argument("to", type=click.IntRange(min=1, clamp=True))
def cli(**kwargs):
    """Parse and handle arguments to run OCR Downloader"""

    click.echo(banner())

    click.echo()

    id_from: int
    id_to: int

    id_from, id_to = kwargs['from'], kwargs['to']

    if id_to is None:
        id_to = id_from

    click.echo(f"From: {id_from}")
    click.echo(f"To: {id_to}")

    tracks = get_tracks(id_from, id_to)

    for track in tracks:
        download(track)


def banner() -> str:
    """Return the banner as a string"""
    return (r'   ____  __________     ____                      __                __         ' + "\n"
            r'  / __ \/ ____/ __ \   / __ \____ _      ______  / /___  ____  ____/ /__  _____' + "\n"
            r' / / / / /   / /_/ /  / / / / __ \ | /| / / __ \/ / __ \/ __ \/ __  / _ \/ ___/' + "\n"
            r'/ /_/ / /___/ _, _/  / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    ' + "\n"
            r'\____/\____/_/ |_|  /_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/  2.0'
            )


if __name__ == "main":
    cli()
