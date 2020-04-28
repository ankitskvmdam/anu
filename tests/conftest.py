"""Package-wide test fixtures."""
from unittest.mock import Mock

from _pytest.config import Config
import pytest
from pytest_mock import MockFixture


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
