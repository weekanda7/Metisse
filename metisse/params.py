# -*- coding=UTF-8 -*-
# pyright: strict
from dataclasses import dataclass, field
from PyQt6 import QtWidgets
from typing import List, Tuple


@dataclass
class ImageRecognitionParams:
    template_image_name: str = ''
    compare_times_counter: int = 1
    screenshot_wait_time: float = 0.1
    accuracy_val: float = 0.9
    is_refresh_screenshot: bool = True
    screen_image_name: str = 'tmp0'
    screen_image_primary_dir: str = 'temp_image'
    screen_image_secondary_dir: str = ''
    screen_image_subdirs: List[str] = field(default_factory=list)
    template_image_primary_dir: str = 'icon'
    template_image_secondary_dir: str = ''
    template_image_subdirs: List[str] = field(default_factory=list)
    is_backup: bool = True
    repeatedly_screenshot_times: int = 1


@dataclass
class SaveParams:
    load_image_primary_dir: str = 'temp_image'
    save_image_primary_dir: str = 'storage'
    save_image_name: str = ''
    screenshot_wait_time: float = 0.1
    compression: float = 1
    load_image_name: str = 'tmp0.png'
    save_image_secondary_dir: str = ''
    save_image_subdirs: List[str] = field(default_factory=list)
    load_image_secondary_dir: str = ''
    load_image_subdirs: List[str] = field(default_factory=list)

    is_save_image_name_add_time: bool = False
    is_refresh_screenshot: bool = True


@dataclass
class DeviceParams:
    device_id: str = ''
    os_environment: str = ''


@dataclass
class UiClientParams:
    image_label: QtWidgets.QLabel = None  # type: ignore
    log_label: QtWidgets.QLabel = None  # type: ignore


@dataclass
class ImageRecognitionResult:
    is_recognized: bool = False
    coordinate: Tuple[int, int] = (0, 0)
    coordinates_list: List[Tuple[int, int]] = field(default_factory=list)
    recognition_threshold: float = 0.9