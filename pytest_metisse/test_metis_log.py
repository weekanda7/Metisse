import logging
import os
import sys
import tempfile
import time

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.utils.metisse_log import MetisseLogger


@pytest.fixture
def test_metis_log_setup():
    """Create a temporary logger and corresponding log file."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        log_file = temp_file.name
        unique_id = int(time.time() * 1000)
        logger_name = "test_logger_{}".format(unique_id)
        metisse_logger = MetisseLogger(
            logger_name=logger_name, log_level=logging.DEBUG, log_file=log_file
        )
    yield metisse_logger, log_file
    metisse_logger.close()
    os.remove(log_file)


def test_log_file_creation(test_metis_log_setup):
    metisse_logger, log_file = test_metis_log_setup
    assert os.path.exists(log_file)


@pytest.mark.parametrize(
    "method,message",
    [
        ("debug", "Test debug message"),
        ("info", "Test info message"),
        ("warning", "Test warning message"),
        ("error", "Test error message"),
        ("critical", "Test critical message"),
    ],
)
def test_log_methods(test_metis_log_setup, method: str, message: str) -> None:
    """Ensure each log method writes the expected message."""

    metisse_logger, log_file = test_metis_log_setup
    getattr(metisse_logger, method)(message)
    _assert_log_contains(message, log_file)


def _assert_log_contains(message, log_file):
    """Check that the log file contains the provided message."""
    with open(log_file, "r") as log_file:
        log_contents = log_file.read()
        assert message in log_contents
