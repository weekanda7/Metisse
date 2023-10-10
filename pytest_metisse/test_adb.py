import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import patch

from metisse.clients.android.adb import AdbClient
from metisse.params import DeviceParams


@pytest.fixture
def adb_client():
    device_params = DeviceParams(
        device_id="test_virtual_device",
        os_environment="android",
    )
    return AdbClient(device_params)


def test_screenshot(adb_client):
    with patch("os.system") as mock_os_system:
        save_screenshot_path = "screenshot.png"
        adb_client.screenshot(save_screenshot_path)

        mock_os_system.assert_any_call(
            f"adb -s {adb_client.device_params.device_id}  shell screencap -p /sdcard/screenshot.png"
        )
        mock_os_system.assert_any_call(
            f"adb -s {adb_client.device_params.device_id}  pull /sdcard/screenshot.png {save_screenshot_path}"
        )


def test_tap(adb_client):
    with patch("os.system") as mock_os_system:
        coordinates = (100, 200)
        adb_client.tap(coordinates)

        mock_os_system.assert_called_once_with(
            f"adb -s {adb_client.device_params.device_id} shell input tap {coordinates[0]} {coordinates[1]}"
        )


def test_swipe(adb_client):
    with patch("os.system") as mock_os_system:
        start_coordinates = (100, 200)
        end_coordinates = (300, 400)
        swiping_time = 1000
        adb_client.swipe(start_coordinates, end_coordinates, swiping_time)

        mock_os_system.assert_called_once_with(
            f"adb -s {adb_client.device_params.device_id} shell input swipe {start_coordinates[0]} {start_coordinates[1]} {end_coordinates[0]} {end_coordinates[1]} {swiping_time}"
        )


if __name__ == "__main__":
    pytest.main(["pytest_metisse/test_adb.py"])
