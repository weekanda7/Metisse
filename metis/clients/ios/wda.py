# -*- coding=UTF-8 -*-
# pyright: strict
from typing import Tuple
import wda  # type: ignore
from ..client import Client
from ...params import DeviceParams


class WdaClient(Client):
    """
    ios client
    """

    def __init__(self, device_params: DeviceParams, skip_wda_launch: bool = False):
        assert device_params.os_environment == 'ios', 'device_params.os_environment must be ios'
        self.device_params = device_params
        if not skip_wda_launch:
            self.wda_client = wda.USBClient(self.device_params.device_id, port=8100)
        self.ios_device_scale = 2
        try:
            self.ios_device_scale = self.wda_client.scale  # type: ignore
        except AttributeError:
            self.ios_device_scale = 2

    def screenshot(self, save_screenshot_path: str) -> None:
        """
        take a screenshot
        """
        self.wda_client.screenshot().save(save_screenshot_path)  # type: ignore

    def tap(self, coordinates: Tuple[int, int]) -> None:
        """
        tap device
        """
        _x, _y = coordinates
        self.wda_client.tap(int(_x / self.ios_device_scale), int(_y / self.ios_device_scale))  # type: ignore

    def swipe(self, start_coordinates: Tuple[int, int], end_coordinates: Tuple[int, int], swiping_time: int) -> None:
        """
        swipe device
        """
        _x, _y = start_coordinates
        _x2, _y2 = end_coordinates
        _ios_swipe_time = float(swiping_time) / 1000
        self.wda_client.swipe(  # type: ignore
            int(_x / self.ios_device_scale),  # type: ignore
            int(_y / self.ios_device_scale),  # type: ignore
            int(_x2 / self.ios_device_scale),  # type: ignore
            int(_y2 / self.ios_device_scale),  # type: ignore
            _ios_swipe_time)  # type: ignore
