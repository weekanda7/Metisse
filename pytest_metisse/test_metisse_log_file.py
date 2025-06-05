import logging
import os
import tempfile

from metisse.utils.metisse_log import MetisseLogger


def test_set_log_file_creates_directory(tmp_path):
    log_dir = tmp_path / "logs"
    log_path = log_dir / "test.log"
    logger = MetisseLogger("test_logger", log_level=logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    logger.set_log_file(str(log_path), formatter)
    assert log_path.exists(), "Log file was not created"
    logger.close()


def test_close_removes_file_handler(tmp_path):
    log_path = tmp_path / "test.log"
    logger = MetisseLogger("test_logger_close", log_level=logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    logger.set_log_file(str(log_path), formatter)
    # ensure file handler is attached
    assert any(isinstance(h, logging.FileHandler) for h in logger.logger.handlers)
    logger.close()
    # after close no file handler should remain
    assert not any(isinstance(h, logging.FileHandler) for h in logger.logger.handlers)
