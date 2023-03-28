# -*- coding=UTF-8 -*-
# pyright: strict
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from cv2 import Mat
from .parms import ImageRecognitionParams, SaveParams


class TemplateMetisClass(ABC):
    """_summary_
        adb fuction template
    Args:
        ABC (_type_): Abstract Base Classes
    """

    @property
    @abstractmethod
    def get_current_root(self) -> str:
        ...

    @property
    @abstractmethod
    def get_device_id(self) -> str:
        ...

    @abstractmethod
    def get_sub_root_path(self, root_key: str) -> str:
        ...

    @abstractmethod
    def _check_image_name_pngFormat(self, _input_name: str) -> str:
        ...

    @abstractmethod
    def _check_path(self, _path: str) -> str:
        ...

    @abstractmethod
    def _set_screen_image_imread_cv2(self,
                                     _screen_image_root_dict_key: str = '',
                                     _image_name: str = '',
                                     _additional_root: str = '') -> None:
        ...

    @abstractmethod
    def _get_screen_image_imread_cv2(self) -> Mat:
        ...

    @abstractmethod
    def _set_template_image_imread_cv2(self,
                                       _template_image_root_dict_key: str = '',
                                       _image_name: str = '',
                                       _additional_root: str = '') -> None:
        ...

    @abstractmethod
    def _get_template_image_imread_cv2(self) -> Mat:
        ...

    @abstractmethod
    def _image_to_position(self, _compared_image_Mat: Mat, _template_image_Mat: Mat, _accuracy_val: float) -> None:
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
    def adb_default_tap(
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
    def save_screenshot_compression(self,
                                    save_params: SaveParams
                                    ) -> None:
        ...

    @abstractmethod
    def crop_screenshot(self, save_params: SaveParams, coordinate1_tuple1: Tuple[int, int], coordinate2_tuple2: Tuple[int, int],
                        ) -> None:
        ...

    @abstractmethod
    def scan_icon_png_to_list(self) -> list[str]:
        ...

    @abstractmethod
    def detect_text(
        self,
        load_image_name: str,
        load_image_root_dict_key: str,
        load_image_additional_root: str,
    ) -> str:
        ...

    @abstractmethod
    def process_itp_center_list(self) -> list[tuple[int, int]] | None:
        ...

    @abstractmethod
    def except_within_range_position(self, _center_list: list[tuple[int, int]] | None, _except_list: list[tuple[int, int]] | None, within_range_x: int, within_range_y: int) -> list[tuple[int, int]] | None:
        ...
