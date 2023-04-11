# -*- coding=UTF-8 -*-
# pyright: strict
from dataclasses import dataclass
from PyQt6 import QtWidgets

@dataclass
class ImageRecognitionParams:
    template_image_name: str = ''
    compare_times_counter: int = 1
    screenshot_wait_time: float = 0.1
    accuracy_val: float = 0.9
    is_refresh_screenshot: bool = True
    screen_image_name: str = 'tmp0'
    screen_image_root_name: str = 'tmp_root'
    screen_image_additional_root_name: str = ''
    template_image_root_name: str = 'icon_root'
    template_image_additional_root_name: str = ''
    is_backup: bool = True
    repeatedly_screenshot_times: int = 1


@dataclass
class SaveParams:
    load_image_root_name: str = 'tmp_root'
    save_image_root_name: str = 'save_root'
    save_image_name: str = ''
    screenshot_wait_time: float = 0.1
    compression: float = 1
    load_image_name: str = 'tmp0.png'
    save_image_additional_root_name: str = ''
    is_save_image_name_add_time: bool = False
    is_refresh_screenshot: bool = True


@dataclass
class DeviceParams:
    device_id: str = ''
    os_environment: str = ''

@dataclass
class UiClientParams:
    image_label: QtWidgets.QLabel = None # type: ignore
    log_label:  QtWidgets.QLabel = None # type: ignore
