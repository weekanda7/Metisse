import os
import sys
from unittest import mock

import numpy as np
import pytest
from PyQt6.QtWidgets import QApplication, QLabel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.params import UiClientParams
from metisse.utils.ui_client import UiClient

app = QApplication(sys.argv)


@pytest.fixture
def ui_client_setup():
    log_label = QLabel()
    image_label = QLabel()
    ui_client_params = UiClientParams(log_label, image_label)
    ui_client = UiClient(ui_client_params)
    yield ui_client, ui_client_params
    del ui_client


def test_send_log_to_ui(ui_client_setup):
    ui_client, ui_client_params = ui_client_setup
    test_log = "Test log message"
    ui_client.send_log_to_ui(test_log)
    assert ui_client_params.log_label.text() == test_log


def test_send_image_path_to_ui(ui_client_setup):
    ui_client, ui_client_params = ui_client_setup
    with mock.patch("cv2.imread") as mock_imread:
        mock_image = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_imread.return_value = mock_image

        test_image_path = "test_image_path.jpg"
        ui_client.send_image_path_to_ui(test_image_path)

        mock_imread.assert_called_once_with(test_image_path)
        assert ui_client_params.image_label.pixmap() is not None


if __name__ == "__main__":
    pytest.main(["-v", "-s", "pytest_metisse/test_ui_client.py"])
