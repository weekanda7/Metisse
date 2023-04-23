import os
import sys
import pytest
from unittest import mock
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.clients.ios.wda import WdaClient
from metisse.params import DeviceParams


@pytest.fixture
def ios_client():
    device_params = DeviceParams(
        device_id="test_virtual_device",
        os_environment="android",
    )
    device_params = DeviceParams(os_environment="ios", device_id="test_virtual_device")
    client = WdaClient(device_params, skip_wda_launch=True)
    return client



@mock.patch("metisse.clients.ios.wda.WdaClient.screenshot")
def test_screenshot(mock_screenshot,ios_client):
    client = ios_client
    save_screenshot_path = "test_screenshot.png"
    client.screenshot(save_screenshot_path)
    mock_screenshot.assert_called_once()

@mock.patch("metisse.clients.ios.wda.WdaClient.tap")
def test_tap(mock_tap,ios_client):
    client = ios_client
    coordinates = (100, 200)
    client.tap(coordinates)
    mock_tap.assert_called_once()

@mock.patch("metisse.clients.ios.wda.WdaClient.swipe")
def test_swipe(mock_swipe,ios_client):
    client = ios_client
    start_coordinates = (100, 200)
    end_coordinates = (300, 400)
    swiping_time = 1.0
    client.swipe(start_coordinates, end_coordinates, swiping_time)
    mock_swipe.assert_called_once()


if __name__ == "__main__":
    pytest.main(['-v','-s','pytest_metisse/test_wdaclient.py'])