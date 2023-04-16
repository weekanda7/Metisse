# -*- coding=UTF-8 -*-
# pyright: strict
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple

from .params import ImageRecognitionParams, SaveParams


class TemplateMetisClass(ABC):
    """_summary_
        adb fuction template
    Args:
        ABC (_type_): Abstract Base Classes
    """

    @property
    @abstractmethod
    def get_device_id(self) -> str:
        ...

    @abstractmethod
    def check_image_recognition(self, params: ImageRecognitionParams) -> bool:
        ...

    @abstractmethod
    def screenshot(
        self,
        save_screenshot_name: str,
        save_screenshot_root_key: str,
        save_screenshot_additional_root: str,
    ) -> None:
        ...

    @abstractmethod
    def tap(self, center: Tuple[int, int], tap_execute_counter_times: int, tap_execute_wait_time: float,
            tap_offset: Tuple[int, int]) -> None:
        ...

    @abstractmethod
    def default_tap(
        self,
        params: ImageRecognitionParams,
        tap_execute_wait_time: float,
        tap_execute_counter_times: int,
        tap_offset: Tuple[int, int],
    ) -> bool:
        ...

    @abstractmethod
    def swipe(
        self,
        center: Tuple[int, int],
        swipe_offset_position: Tuple[int, int],
        swiping_time: int,
        swipe_execute_counter_times: int,
        swipe_execute_wait_time: float,
    ) -> None:
        ...

    @abstractmethod
    def press(
        self,
        center: Tuple[int, int],
        pressing_time: int,
        press_execute_counter_times: int,
        press_execute_wait_time: float,
    ) -> None:
        ...

    @abstractmethod
    def save_screenshot_compression(self, save_params: SaveParams) -> None:
        ...

    @abstractmethod
    def crop_screenshot(
        self,
        coordinate1_tuple1: Tuple[int, int],
        coordinate2_tuple2: Tuple[int, int],
        save_params: SaveParams,
    ) -> None:
        ...

