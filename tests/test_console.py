"""Test cases for the console module."""
from unittest.mock import Mock

from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests

from hypermodern_python import console


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0
