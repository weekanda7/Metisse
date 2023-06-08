# -*- coding=UTF-8 -*-
# pyright: strict
"""
This module contains functions for android and ios script.
It includes device port connect, screen shoot ,image similarity calculation, device control.
"""

from __future__ import annotations
import logging
import os
import time
try:
    import wda  # type: ignore
except ImportError:
    print('No module')
from typing import Tuple
# pylint: disable=no-member
from PIL import Image
import inspect
from .params import ImageRecognitionParams, SaveParams, DeviceParams, UiClientParams, ImageRecognitionResult
from .template_metis import TemplateMetisClass
from .clients.ios.wda import WdaClient
from .clients.android.adb import AdbClient
from .utils.metisse_path import DevPath
from .utils.opencv_utils import Opencv_utils
from .utils.ui_client import UiClient
from .utils.metisse_log import MetisseLogger
from .utils import image_recognition
from .settings import Settings as ST


class MetisseClass(TemplateMetisClass):

    def __init__(self, device_id: str, relatively_path: str, pyqt6_ui_label: UiClientParams, os_environment: str = 'android'):
        assert device_id != ''
        if not relatively_path:
            self._relatively_path = MetisseClass.get_current_path()
        else:
            self._relatively_path = relatively_path

        super(TemplateMetisClass, self).__init__()

        self._device_id = self.check_device_id_path_valid(device_id)
        self._dev_path = DevPath(self._relatively_path)
        self._script_path = self._dev_path.create_extended_script_path(self._device_id)
        self._logger = MetisseLogger("MetisClass_logger",
                                     log_level=logging.DEBUG,
                                     log_file=os.path.join(self._script_path.device_id_path, "log",
                                                           self.get_time() + self._device_id + ".log"))
        assert os_environment in ST.OS_ENVIRONMENT
        self._os_environment = os_environment  # android , ios
        self.ios_device_scale = 2  # init var

        if self._os_environment == 'ios':
            self._client = WdaClient(DeviceParams(device_id, os_environment))
        elif self._os_environment == 'android':
            self._client = AdbClient(DeviceParams(device_id, os_environment))
        else:
            raise ValueError('os_environment must be android or ios')
        self._img_recog_result = ImageRecognitionResult()

        self._ui_client = UiClient(pyqt6_ui_label)

        self.is_backup = False
        self.backup_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        assert isinstance(self.backup_time, str)
        self.screenshot_wait_time_increase: float = 1
        self.is_check_gamelog: bool = False

    @staticmethod
    def get_current_path() -> str:
        """
        get current path
        """
        caller_frame = inspect.stack()[2]
        caller_file_path = caller_frame.filename
        _path = os.path.dirname(os.path.abspath(caller_file_path))
        return _path

    def execute_time_sleep(self, wait_time: float = 0):
        self._logger.info("execute_time_sleep : wait_time= %.2f", wait_time)
        self._ui_client.send_log_to_ui(f"execute_time_sleep method : \n wait_time= {wait_time:.2f}")
        time.sleep(wait_time)

    def check_device_id_path_valid(self,input:str) -> str:
        if ':' in input:
            return input.replace(':', '_')
        return input

    @property
    def get_device_id(self) -> str:
        if self._device_id:
            return ' -s ' + self._device_id
        return ''

    def check_gamelog(self, params: ImageRecognitionParams):
        params.template_image_name = 'log_button'
        try:
            _screen_image_path = self._script_path.get_screen_image_path(params)
            if not os.path.isfile(_screen_image_path):
                self.screenshot()
            _template_image_path = self._script_path.get_template_image_path(params)
            if not os.path.isfile(_template_image_path):
                raise FileNotFoundError(f"FileNotFoundError: {_template_image_path}")
            self.opencv_utils = Opencv_utils(_screen_image_path, _template_image_path)
            self._img_recog_result = image_recognition.match_template(self.opencv_utils.screen_image_mat,
                                                                      self.opencv_utils.template_image_mat, params.accuracy_val)
        except FileNotFoundError as error_msg:
            self._logger.info("FileNotFoundError: %s", error_msg)
        except Exception as error:
            self._logger.error("An unexpected error occurred: %s", error)

        if self._img_recog_result.is_recognized:
            self._logger.info("match_template method : template_name=%s prob=%.4f accuracy_val=%.4f %s",
                              params.template_image_name, self._img_recog_result.recognition_threshold, params.accuracy_val,
                              self._img_recog_result.is_recognized)
            self._ui_client.send_image_path_to_ui(_image_path=_template_image_path)
            self._ui_client.send_log_to_ui(
                f"match_template method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n accuracy_val={params.accuracy_val:.4f} \n {self._img_recog_result.is_recognized}"
            )
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(
                    SaveParams(
                        save_image_primary_dir='storage',
                        save_image_name=
                        f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
                        save_image_secondary_dir=self.backup_time,
                        is_refresh_screenshot=False))
            self.tap(self._img_recog_result.coordinate)

    def get_time(self) -> str:
        return time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime())

    def screenshot(
        self,
        save_screenshot_name: str = 'tmp0.png',
        save_screenshot_root_key: str = 'temp_image',
        save_screenshot_additional_root: str = '',
    ) -> None:

        if self._os_environment == 'android':

            self._client.screenshot(
                f"{self._script_path.get_image_path(save_screenshot_name,save_screenshot_root_key,save_screenshot_additional_root)}"
            )
        elif self._os_environment == 'ios':
            self._client.screenshot(
                f"{self._script_path.get_image_path(save_screenshot_name,save_screenshot_root_key,save_screenshot_additional_root)}"
            )
        else:
            raise RuntimeError("Unsupported OS environment")
        self._logger.debug("adb_screenshot method : process %s", save_screenshot_name)
        self._ui_client.send_log_to_ui(f"adb_screenshot method : \n process {save_screenshot_name:s}")

    def check_image_recognition(self, params: ImageRecognitionParams) -> bool:
        save_params = SaveParams(
            save_image_primary_dir='storage',
            save_image_name=
            f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
            save_image_secondary_dir=self.backup_time,
            is_refresh_screenshot=False)

        def _single_time() -> bool:
            if params.compare_times_counter > 1 and params.is_refresh_screenshot is False:
                self._logger.info('warring efficient lost')
            for _num in range(params.compare_times_counter):
                if self.is_check_gamelog:
                    self.check_gamelog(ImageRecognitionParams())
                if params.is_refresh_screenshot:
                    time.sleep(params.screenshot_wait_time + self.screenshot_wait_time_increase)
                    self.screenshot(params.screen_image_name, params.screen_image_primary_dir,
                                    params.screen_image_secondary_dir)

                _screen_image_path = self._script_path.get_screen_image_path(params)
                _template_image_path = self._script_path.get_template_image_path(params)
                self.opencv_utils = Opencv_utils(_screen_image_path, _template_image_path)
                self._img_recog_result = image_recognition.match_template(self.opencv_utils.screen_image_mat,
                                                                          self.opencv_utils.template_image_mat,
                                                                          params.accuracy_val)

                self._logger.info("image_recognition method : template_name=%s  prob=%.4f accuracy_val=%.4f %s",
                                  params.template_image_name, self._img_recog_result.recognition_threshold, params.accuracy_val,
                                  self._img_recog_result.is_recognized)
                self._ui_client.send_image_path_to_ui(_image_path=_template_image_path)
                self._ui_client.send_log_to_ui(
                    f"image_recognition method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n accuracy_val={params.accuracy_val:.4f} \n {self._img_recog_result.is_recognized}"
                )
                if self._img_recog_result.is_recognized:
                    if self.is_backup and params.is_backup:
                        self.save_screenshot_compression(save_params)
                    return True
            return False

        def _multiple_times() -> bool:
            _screen_image_name_list = [f'tmp{x}' for x in range(params.repeatedly_screenshot_times)]
            if self.is_check_gamelog:
                self.check_gamelog(ImageRecognitionParams())
            _template_image_path = self._script_path.get_template_image_path(params)
            time.sleep(params.screenshot_wait_time + self.screenshot_wait_time_increase)

            for _num in range(params.compare_times_counter):
                for _temp_screen_image_name in _screen_image_name_list:

                    self.screenshot(_temp_screen_image_name, params.screen_image_primary_dir, params.screen_image_secondary_dir)
                for _temp_screen_image_name in _screen_image_name_list:
                    _screen_image_path = self._script_path.get_screen_image_path(params)
                    params.screen_image_name = _temp_screen_image_name
                    self.opencv_utils = Opencv_utils(_screen_image_path, _template_image_path)
                    self._img_recog_result = image_recognition.match_template(self.opencv_utils.screen_image_mat,
                                                                              self.opencv_utils.template_image_mat,
                                                                              params.accuracy_val)
                    self._logger.info("match_template method : template_name=%s  prob=%.4f accuracy_val=%.4f %s",
                                      params.template_image_name, self._img_recog_result.recognition_threshold,
                                      params.accuracy_val, self._img_recog_result.is_recognized)
                    self._ui_client.send_image_path_to_ui(_image_path=_template_image_path)
                    self._ui_client.send_log_to_ui(
                        f"match_template method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n accuracy_val={params.accuracy_val:.4f} \n {self._img_recog_result.is_recognized}"
                    )
                    if self._img_recog_result.is_recognized:
                        if self.is_backup and params.is_backup:
                            self.save_screenshot_compression(save_params)
                        return True
            return False

        if params.repeatedly_screenshot_times <= 1:
            if _single_time():
                return True
        else:
            if _multiple_times():
                return True
        if self.is_backup and params.is_backup:
            self.save_screenshot_compression(save_params)
        return False

    def tap(
            self,
            center: Tuple[int, int],
            tap_execute_counter_times: int = 1,
            tap_execute_wait_time: float = 0,
            tap_offset: Tuple[int, int] = (0, 0),
    ) -> None:

        for _tap_time in range(tap_execute_counter_times):
            time.sleep(tap_execute_wait_time)
            (_x, _y) = center
            _x += tap_offset[0]
            _y += tap_offset[1]
            self._client.tap((_x, _y))
            self._logger.info("tap method : (x,y) = %s offset = %s", center, tap_offset)
            self._ui_client.send_log_to_ui(f"tap method : \n (x,y) = {center} \n offset = {tap_offset}")

    def swipe(
        self,
        center: Tuple[int, int],
        swipe_offset_position: Tuple[int, int],
        swiping_time: int = 300,
        swipe_execute_counter_times: int = 1,
        swipe_execute_wait_time: float = 0,
    ) -> None:

        for _swipe_time in range(swipe_execute_counter_times):
            time.sleep(swipe_execute_wait_time)
            (_x, _y) = center
            (_x2, _y2) = swipe_offset_position
            self._client.swipe((_x, _y), (_x2, _y2), swiping_time)
            self._logger.info("swipe method : (x,y) = %s (x2,y2) = %s swiping_time = %.2f", center, swipe_offset_position,
                              swiping_time)
            self._ui_client.send_log_to_ui(
                f"swipe method : \n (x,y) = {center} \n (x2,y2) = {swipe_offset_position} \n swiping_time = {swiping_time}")

    def press(
        self,
        center: Tuple[int, int],
        pressing_time: int = 400,
        press_execute_counter_times: int = 1,
        press_execute_wait_time: float = 0,
    ) -> None:

        for _swipe_time in range(press_execute_counter_times):
            try:
                time.sleep(press_execute_wait_time)
                self.swipe(center, center, pressing_time)
                self._logger.info("adb_press method : (x,y) = %s pressing_time = %d", center, pressing_time)
                self._ui_client.send_log_to_ui(f"adb_press method : \n (x,y) = {center} \n pressing_time = {pressing_time}")
            except OSError as error_msg:
                self._logger.exception("adb_press method :  %s", error_msg)
                self._ui_client.send_log_to_ui(f"adb_press method : \n {error_msg}")

    def default_tap(
            self,
            params: ImageRecognitionParams,
            tap_execute_wait_time: float = 0.1,
            tap_execute_counter_times: int = 1,
            tap_offset: Tuple[int, int] = (0, 0),
    ) -> bool:
        save_params = SaveParams(
            save_image_primary_dir='storage',
            save_image_name=
            f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
            save_image_secondary_dir=self.backup_time,
            is_refresh_screenshot=False)
        if self.check_image_recognition(params):
            self.tap(self._img_recog_result.coordinate, tap_execute_counter_times, tap_execute_wait_time, tap_offset)
            self._logger.info("default_tap method : template_name=%s  prob=%.4f %s", params.template_image_name,
                              self._img_recog_result.recognition_threshold, self._img_recog_result.is_recognized)
            self._ui_client.send_log_to_ui(
                f"default_tap method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n {self._img_recog_result.is_recognized}"
            )
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(save_params)
            return True

        self._logger.info("default_tap method : template_name=%s  prob=%.4f %s", params.template_image_name,
                          self._img_recog_result.recognition_threshold, self._img_recog_result.is_recognized)
        self._ui_client.send_log_to_ui(
            f"default_tap method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n {self._img_recog_result.is_recognized}"
        )
        if self.is_backup and params.is_backup:
            self.save_screenshot_compression(save_params)
        return False

    def default_swipe(
        self,
        params: ImageRecognitionParams,
        swipe_offset_position: Tuple[int, int] = (0, 0),
        swiping_time: int = 300,
        swipe_execute_counter_times: int = 1,
        swipe_execute_wait_time: float = 0,
    ) -> bool:
        save_params = SaveParams(
            save_image_primary_dir='storage',
            save_image_name=
            f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
            save_image_secondary_dir=self.backup_time,
            is_refresh_screenshot=False)
        if self.check_image_recognition(params):
            self.swipe(self._img_recog_result.coordinate, swipe_offset_position, swiping_time, swipe_execute_counter_times,
                       swipe_execute_wait_time)
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(save_params)
            return True

        if self.is_backup and params.is_backup:
            self.save_screenshot_compression(save_params)
        return False

    def default_press(
        self,
        params: ImageRecognitionParams,
        pressing_time: int = 300,
        press_execute_counter_times: int = 1,
        press_execute_wait_time: float = 0,
    ) -> bool:
        save_params = SaveParams(
            save_image_primary_dir='storage',
            save_image_name=
            f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
            save_image_secondary_dir=self.backup_time,
            is_refresh_screenshot=False)
        if self.check_image_recognition(params):
            self.press(self._img_recog_result.coordinate, pressing_time, press_execute_counter_times, press_execute_wait_time)
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(save_params)
            return True

        if self.is_backup and params.is_backup:
            self.save_screenshot_compression(save_params)
        return False

    def save_screenshot_compression(self, save_params: SaveParams) -> None:
        if save_params.is_refresh_screenshot:
            time.sleep(save_params.screenshot_wait_time)
            self.screenshot()
        _img = Image.open(self._script_path.get_load_image_path(save_params))
        if save_params.is_save_image_name_add_time:
            _save_png_image_name = self.get_time() + save_params.save_image_name + '.png'
        else:
            _save_png_image_name = save_params.save_image_name + '.png'
        save_params.save_image_name = _save_png_image_name
        _image_path = self._script_path.get_save_image_path(save_params)
        self._script_path.check_path(os.path.dirname(_image_path))

        if save_params.compression != 1:
            (_w, _h) = _img.size
            _w = int(_w * save_params.compression)
            _h = int(_h * save_params.compression)
            _new_resize_img = _img.resize((_w, _h))
            _new_resize_img.save(_image_path)
            if not self.is_backup:
                self._logger.info("save_screenshot_compression method : raw data w=%d, h=%d compression = %.2f name=%s ", _w,
                                  _h, save_params.compression, _save_png_image_name)
                self._ui_client.send_log_to_ui(
                    f"save_screenshot_compression method :\n raw data w={_w}, h={_h}\n compression = {save_params.compression}\n name={_save_png_image_name} "
                )
        else:
            (_w, _h) = _img.size
            _img.save(_image_path)
            if not self.is_backup:
                self._logger.info("save_screenshot_compression method : raw data w=%d, h=%d name=%s", _w, _h,
                                  _save_png_image_name)
                self._ui_client.send_log_to_ui(
                    f"save_screenshot_compression method : \n raw data w={_w}, h={_h} \n name={_save_png_image_name}")

    def crop_screenshot(
        self,
        coordinate1_tuple1: Tuple[int, int],
        coordinate2_tuple2: Tuple[int, int],
        save_params: SaveParams,
    ) -> None:

        if save_params.is_refresh_screenshot:
            time.sleep(save_params.screenshot_wait_time)
            self.screenshot()
        _img = Image.open(self._script_path.get_load_image_path(save_params))
        _pos_x, _pos_y = coordinate1_tuple1
        _pos_x2, _pos_y2 = coordinate2_tuple2

        _pos_x2 -= _pos_x
        _pos_y2 -= _pos_y
        _region = (_pos_x, _pos_y, _pos_x + _pos_x2, _pos_y + _pos_y2)
        _crop_img = _img.crop(_region)
        if save_params.is_save_image_name_add_time:
            _save_png_image_name = self.get_time() + save_params.save_image_name + '.png'
        else:
            _save_png_image_name = save_params.save_image_name + '.png'

        save_params.save_image_name = _save_png_image_name
        _image_path = self._script_path.get_save_image_path(save_params)
        self._script_path.check_path(os.path.dirname(_image_path))
        _crop_img.save(_image_path)
        self._logger.info("crop_screenshot method : exported : w=%s", _save_png_image_name)
        self._ui_client.send_log_to_ui(f"crop_screenshot method : \n exported : w={_save_png_image_name}")
