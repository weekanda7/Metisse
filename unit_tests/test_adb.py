import os
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import patch
from metis.clients.andriod.adb import AdbClient
from metis.params import DeviceParams


class TestAdbClient(unittest.TestCase):
    def setUp(self):
        device_params = DeviceParams(
            device_id="test_virtual_device",
            os_environment="android",
        )
        self.adb_client = AdbClient(device_params)

    @patch("os.system")
    def test_screenshot(self, mock_os_system):
        save_screenshot_path = "screenshot.png"
        self.adb_client.screenshot(save_screenshot_path)

        mock_os_system.assert_any_call(
            f"adb -s {self.adb_client.device_params.device_id}  shell screencap -p /sdcard/screenshot.png"
        )
        mock_os_system.assert_any_call(
            f"adb -s {self.adb_client.device_params.device_id}  pull /sdcard/screenshot.png {save_screenshot_path}"
        )

    @patch("os.system")
    def test_tap(self, mock_os_system):
        coordinates = (100, 200)
        self.adb_client.tap(coordinates)

        mock_os_system.assert_called_once_with(
            f"adb -s {self.adb_client.device_params.device_id} shell input tap {coordinates[0]} {coordinates[1]}"
        )

    @patch("os.system")
    def test_swipe(self, mock_os_system):
        start_coordinates = (100, 200)
        end_coordinates = (300, 400)
        swiping_time = 1000
        self.adb_client.swipe(start_coordinates, end_coordinates, swiping_time)

        mock_os_system.assert_called_once_with(
            f"adb -s {self.adb_client.device_params.device_id} shell input swipe {start_coordinates[0]} {start_coordinates[1]} {end_coordinates[0]} {end_coordinates[1]} {swiping_time}"
        )


if __name__ == "__main__":
    unittest.main()