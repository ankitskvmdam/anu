"""Test cases for the console module."""
from unittest.mock import Mock

from click.testing import CliRunner
import pytest

from anu.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(main.main)
    assert result.exit_code == 0
