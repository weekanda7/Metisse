import sys
import time
import pytest
import tempfile
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.utils.metisse_log import MetisseLogger



@pytest.fixture
def test_metis_log_setup():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        log_file = temp_file.name
        unique_id = int(time.time() * 1000)
        logger_name = "test_logger_{}".format(unique_id)
        metisse_logger = MetisseLogger(logger_name=logger_name, log_level=logging.DEBUG, log_file=log_file)
    yield metisse_logger, log_file
    metisse_logger.close()
    os.remove(log_file)

def test_log_file_creation(test_metis_log_setup):
    metisse_logger, log_file = test_metis_log_setup
    assert os.path.exists(log_file)

def test_log_debug_message(test_metis_log_setup):
    metisse_logger, log_file = test_metis_log_setup
    message = "Test debug message"
    metisse_logger.debug(message)
    _assert_log_contains(message, log_file)

def test_log_info_message(test_metis_log_setup):
    metisse_logger, log_file = test_metis_log_setup
    message = "Test info message"
    metisse_logger.info(message)
    _assert_log_contains(message, log_file)

def test_log_warning_message(test_metis_log_setup):
    metisse_logger, log_file = test_metis_log_setup
    message = "Test warning message"
    metisse_logger.warning(message)
    _assert_log_contains(message, log_file)

def test_log_error_message(test_metis_log_setup):
    metisse_logger, log_file = test_metis_log_setup
    message = "Test error message"
    metisse_logger.error(message)
    _assert_log_contains(message, log_file)

def test_log_critical_message(test_metis_log_setup):
    metisse_logger, log_file = test_metis_log_setup
    message = "Test critical message"
    metisse_logger.critical(message)
    _assert_log_contains(message, log_file)

def _assert_log_contains(message, log_file):
    with open(log_file, "r") as log_file:
        log_contents = log_file.read()
        assert message in log_contents


if __name__ == "__main__":
    pytest.main(['-v','-s','pytest_metisse/test_metis_log.py'])