from click.testing import CliRunner
from pytest_mock import MockerFixture

from ocrdownloader2 import cli
from ocrdownloader2.data.track import Track


def test_cli(mocker: MockerFixture) -> None:
    runner = CliRunner()

    get_tracks = mocker.patch(
        "ocrdownloader2.cli.get_tracks",
        return_value=[
            Track(
                id=1,
                title="Track 1",
                authors=[],
                links={"https://example.com/"},
                checksum="abc123",
            ),
            Track(
                id=2,
                title="Track 2",
                authors=[],
                links={"https://example.com/"},
                checksum="abc123",
            ),
        ],
    )

    get_engine = mocker.patch("ocrdownloader2.cli.get_engine", autospec=True)

    result = runner.invoke(cli.cli, ["1", "2"])

    assert result.exit_code == 0

    get_tracks.assert_called_once_with(1, 2)
    get_engine.assert_called_once()


def test_cli_with_single_id(mocker: MockerFixture) -> None:
    runner = CliRunner()

    get_tracks = mocker.patch(
        "ocrdownloader2.cli.get_tracks",
        return_value=[
            Track(
                id=1,
                title="Track 1",
                authors=[],
                links={"https://example.com/"},
                checksum="abc123",
            ),
        ],
    )

    get_engine = mocker.patch("ocrdownloader2.cli.get_engine", autospec=True)

    result = runner.invoke(cli.cli, ["1"])

    assert result.exit_code == 0

    get_tracks.assert_called_once_with(1, 1)
    get_engine.assert_called_once()
