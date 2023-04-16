import os
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.clients.ios.wda import WdaClient
from metisse.params import DeviceParams


class TestWdaClient(unittest.TestCase):

    def setUp(self):
        self.device_params = DeviceParams(os_environment="ios", device_id="test_virtual_device")
        self.client = WdaClient(self.device_params, skip_wda_launch=True)
        self.client.wda_client = MagicMock()  # Add this line to create a mock object for wda_client

    @mock.patch("metisse.clients.ios.wda.WdaClient.screenshot")
    def test_screenshot(self, mock_screenshot):
        save_screenshot_path = "test_screenshot.png"
        self.client.screenshot(save_screenshot_path)
        mock_screenshot.assert_called_once()

    @mock.patch("metisse.clients.ios.wda.WdaClient.tap")
    def test_tap(self, mock_tap):
        coordinates = (100, 200)
        self.client.tap(coordinates)
        mock_tap.assert_called_once()

    @mock.patch("metisse.clients.ios.wda.WdaClient.swipe")
    def test_swipe(self, mock_swipe):
        start_coordinates = (100, 200)
        end_coordinates = (300, 400)
        swiping_time = 1.0
        self.client.swipe(start_coordinates, end_coordinates, swiping_time)
        mock_swipe.assert_called_once()


if __name__ == "__main__":
    unittest.main()