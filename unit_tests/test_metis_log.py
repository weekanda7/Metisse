import sys
import unittest
import tempfile
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metis.utils.metis_log import MetisLogger

class TestMetisLogger(unittest.TestCase):

    def setUp(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            self.log_file = temp_file.name
        self.logger_name = "test_logger"
        self.metis_logger = MetisLogger(logger_name=self.logger_name, log_level=logging.DEBUG, log_file=self.log_file)

    def tearDown(self):
        self.metis_logger.close()
        os.remove(self.log_file)

    def test_log_file_creation(self):
        self.assertTrue(os.path.exists(self.log_file))

    def test_log_debug_message(self):
        message = "Test debug message"
        self.metis_logger.debug(message)
        self._assert_log_contains(message)

    def test_log_info_message(self):
        message = "Test info message"
        self.metis_logger.info(message)
        self._assert_log_contains(message)

    def test_log_warning_message(self):
        message = "Test warning message"
        self.metis_logger.warning(message)
        self._assert_log_contains(message)

    def test_log_error_message(self):
        message = "Test error message"
        self.metis_logger.error(message)
        self._assert_log_contains(message)

    def test_log_critical_message(self):
        message = "Test critical message"
        self.metis_logger.critical(message)
        self._assert_log_contains(message)

    def _assert_log_contains(self, message):
        with open(self.log_file, "r") as log_file:
            log_contents = log_file.read()
            self.assertIn(message, log_contents)

if __name__ == "__main__":
    unittest.main()