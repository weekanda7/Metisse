import os
import shutil
import sys
import tempfile
from unittest import mock
from unittest.mock import patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtWidgets import QApplication, QLabel

from metisse.clients.android import AdbClient
from metisse.clients.ios import WdaClient
from metisse.metisse import MetisseClass
from metisse.params import DeviceParams, UiClientParams
from metisse.utils.metisse_path import DevPath
from metisse.utils.ui_client import UiClient

app = QApplication(sys.argv)


@pytest.fixture
def test_metisse_class_test_dir():
    test_dir = tempfile.mkdtemp()
    yield test_dir
    shutil.rmtree(test_dir)


def test_metisse_class_init_android(test_metisse_class_test_dir):
    test_dir = test_metisse_class_test_dir

    device_id = "test_virtual_device"
    relatively_path = test_dir
    pyqt6_ui_label = UiClient(UiClientParams(QLabel(), QLabel()))
    os_environment = "android"
    with patch(
        "metisse.utils.metisse_log.MetisseLogger.__init__", return_value=None
    ) as mock_metisse_log_init:
        metisse = MetisseClass(
            device_id, relatively_path, pyqt6_ui_label, os_environment
        )
        mock_metisse_log_init.assert_called_once()
        assert metisse._device_id == device_id
        assert metisse._relatively_path == test_dir
        assert isinstance(metisse._ui_client, UiClient)
        assert metisse._os_environment == os_environment
        assert isinstance(metisse._client, AdbClient)


def test_metisse_class_init_ios(test_metisse_class_test_dir):
    test_dir = test_metisse_class_test_dir
    # Test for iOS
    device_id = "test_virtual_device"
    relatively_path = test_dir
    pyqt6_ui_label = None
    os_environment_ios = "ios"
    with patch(
        "metisse.utils.metisse_log.MetisseLogger.__init__", return_value=None
    ) as mock_metisse_log_init, patch(
        "metisse.clients.ios.wda.WdaClient.__init__", return_value=None
    ) as mock_wda_client_init:
        metisse_ios = MetisseClass(
            device_id, relatively_path, pyqt6_ui_label, os_environment_ios
        )
        mock_wda_client_init.assert_called_once()
        mock_metisse_log_init.assert_called_once()
    assert metisse_ios._os_environment == os_environment_ios
    assert isinstance(metisse_ios._client, WdaClient)


def test_metisse_class_init_invalid_os(test_metisse_class_test_dir):
    test_dir = test_metisse_class_test_dir
    # Test for invalid os_environment
    device_id = "test_virtual_device"
    relatively_path = test_dir
    pyqt6_ui_label = None
    os_environment_invalid = "invalid"
    with patch(
        "metisse.utils.metisse_log.MetisseLogger.__init__", return_value=None
    ) as mock_metisse_log_init:
        with pytest.raises(AssertionError):
            MetisseClass(
                device_id, relatively_path, pyqt6_ui_label, os_environment_invalid
            )
            mock_metisse_log_init.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v", "-s", "pytest_metisse/test_metisse_class.py"])
