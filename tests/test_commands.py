import pytest
from click.testing import CliRunner
from py_compose.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0
