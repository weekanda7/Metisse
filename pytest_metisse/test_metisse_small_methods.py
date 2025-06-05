import os
import shutil
from unittest import mock

import pytest

from metisse.metisse import MetisseClass
from metisse.params import UiClientParams


@pytest.fixture
def metisse_basic_setup(tmp_path):
    test_metisse = MetisseClass(
        device_id="device:123",
        relatively_path=str(tmp_path),
        pyqt6_ui_label=UiClientParams(),
        os_environment="android",
    )
    test_metisse._logger.close()
    yield test_metisse
    shutil.rmtree(str(tmp_path))


def test_check_device_id_path_valid(metisse_basic_setup):
    result = metisse_basic_setup.check_device_id_path_valid("abc:123")
    assert result == "abc_123"
    assert metisse_basic_setup._device_id == "device_123"


def test_get_device_id_property(metisse_basic_setup):
    assert metisse_basic_setup.get_device_id == " -s device_123"


@mock.patch("metisse.metisse.time.sleep")
def test_execute_time_sleep(mock_sleep, metisse_basic_setup):
    with mock.patch.object(
        metisse_basic_setup._logger, "info"
    ) as mock_info, mock.patch.object(
        metisse_basic_setup._ui_client, "send_log_to_ui"
    ) as mock_send:
        metisse_basic_setup.execute_time_sleep(1.5)
        mock_info.assert_called_with("execute_time_sleep : wait_time= %.2f", 1.5)
        mock_send.assert_called_with("execute_time_sleep method : \n wait_time= 1.50")
        mock_sleep.assert_called_once_with(1.5)


@mock.patch("metisse.metisse.time.strftime", return_value="2025-01-01_00_00_00_")
def test_get_time(mock_strftime, metisse_basic_setup):
    result = metisse_basic_setup.get_time()
    assert result == "2025-01-01_00_00_00_"
    mock_strftime.assert_called_once()


def _wrapper_for_current_path() -> str:
    """Helper used to test ``get_current_path``."""
    return MetisseClass.get_current_path()


def test_get_current_path():
    expected = os.path.dirname(os.path.abspath(__file__))
    assert _wrapper_for_current_path() == expected
