from unittest import mock

import pytest

from metisse.clients.ios.wda import WdaClient
from metisse.params import DeviceParams


@mock.patch("metisse.clients.ios.wda.wda.USBClient")
def test_wdaclient_methods(mock_usbclient):
    mock_instance = mock.MagicMock()
    mock_instance.scale = 3
    mock_usbclient.return_value = mock_instance

    dp = DeviceParams(device_id="iosdev", os_environment="ios")
    client = WdaClient(dp)

    img_mock = mock.MagicMock()
    mock_instance.screenshot.return_value = img_mock

    client.screenshot("out.png")
    mock_instance.screenshot.assert_called_once()
    img_mock.save.assert_called_once_with("out.png")

    client.tap((30, 60))
    mock_instance.tap.assert_called_once_with(10, 20)

    client.swipe((30, 60), (90, 120), 1000)
    mock_instance.swipe.assert_called_once_with(10, 20, 30, 40, 1.0)
