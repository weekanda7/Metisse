# -*- coding=UTF-8 -*-
# pyright: strict
import os
from typing import Tuple
from ..client import Client
from ...params import DeviceParams


class AdbClient(Client):
    """
    android client
    """

    def __init__(self, device_params: DeviceParams):
        assert device_params.os_environment == 'android', 'device_params.os_environment must be android'
        self.device_params = device_params

    def screenshot(self, save_screenshot_path: str) -> None:
        """
        take a screenshot
        """
        os.system(f"adb -s {self.device_params.device_id}  shell screencap -p /sdcard/screenshot.png")
        os.system(f"adb -s {self.device_params.device_id}  pull /sdcard/screenshot.png {save_screenshot_path}")

    def tap(self, coordinates: Tuple[int, int]) -> None:
        """
        tap device
        """
        _x, _y = coordinates
        os.system(f"adb -s {self.device_params.device_id} shell input tap {_x} {_y}")

    def swipe(self, start_coordinates: Tuple[int, int], end_coordinates: Tuple[int, int], swiping_time: int) -> None:
        """
        swipe device
        """
        _x, _y = start_coordinates
        _x2, _y2 = end_coordinates
        os.system(f"adb -s {self.device_params.device_id} shell input swipe {_x} {_y} {_x2} {_y2} {swiping_time}")