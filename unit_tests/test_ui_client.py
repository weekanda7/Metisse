import os
import sys
import unittest
from unittest.mock import MagicMock
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.params import UiClientParams
from core.utils.ui_client import UiClient

app = QApplication(sys.argv)


class TestUiClient(unittest.TestCase):

    def setUp(self):
        self.log_label = QLabel()
        self.image_label = QLabel()
        self.ui_client_params = UiClientParams(self.log_label, self.image_label)
        self.ui_client = UiClient(self.ui_client_params)

    def test_send_log_to_ui(self):
        test_log = "Test log message"
        self.ui_client.send_log_to_ui(test_log)
        self.assertEqual(self.ui_client_params.log_label.text(), test_log)

    def test_send_image_path_to_ui(self):
        with unittest.mock.patch("cv2.imread") as mock_imread:
            mock_image = np.zeros((100, 100, 3), dtype=np.uint8)
            mock_imread.return_value = mock_image

            test_image_path = "test_image_path.jpg"
            self.ui_client.send_image_path_to_ui(test_image_path)

            mock_imread.assert_called_once_with(test_image_path)
            self.assertIsNotNone(self.ui_client_params.image_label.pixmap())

    def tearDown(self):
        del self.ui_client

if __name__ == "__main__":
    unittest.main()