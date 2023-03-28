# -*- coding=UTF-8 -*-
# pyright: strict
"""
This module contains functions for android and ios script.
It includes device port connect, screen shoot ,image similarity calculation, device control.
version 2.12.2
"""

from __future__ import annotations
from .params import ImageRecognitionParams, SaveParams
from .template_metis import TemplateMetisClass
import io
import logging
import os
import time
try:
    from PyQt6 import QtWidgets
    from PyQt6.QtGui import QImage, QPixmap
    import wda  # type: ignore
except ImportError:
    print('No module')
from os import listdir
from os.path import isdir, isfile, join
from pathlib import Path
from typing import Dict, Tuple
import cv2
import numpy as np  # type: ignore
# pylint: disable=no-member
from cv2 import Mat
from PIL import Image
import natsort
from google.cloud import vision  # type: ignore
from .params import ImageRecognitionParams, SaveParams
from .template_metis import TemplateMetisClass

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fine_key.json'

OS_ENVIRONMENT = ['android', 'ios']


class MetisClass(TemplateMetisClass):

    def __init__(self,
                 device_id: str,
                 sub_root_dict: Dict[str, str],
                 relatively_path: str,
                 pyqt6_ui_label_dict: Dict[str, QtWidgets.QLabel],
                 os_environment: str = 'android'):
        self._relatively_path = relatively_path
        super(TemplateMetisClass, self).__init__()

        self._device_id = device_id
        self._sub_root_dict = sub_root_dict
        for _key, _value in self._sub_root_dict.items():
            if ':' in _value:
                self._sub_root_dict[_key] = _value.replace(':', '_')
        assert os_environment in OS_ENVIRONMENT
        self._os_environment = os_environment  # android , ios
        self.ios_device_scale = 2  # init var
        self.ios_device_scale = 2  # init var
        if self._os_environment == 'ios':
            self.wda_client = wda.USBClient(device_id, port=8100)
            try:
                self.ios_device_scale = self.wda_client.scale  # type: ignore
            except AttributeError:
                self.ios_device_scale = 2
        self._log()
        self._screen_image_Mat: Mat
        self._template_image_Mat: Mat
        self._itp_bool = False
        self._itp_center = (0, 0)
        self._itp_center_list: list[tuple[int, int]]
        self._itp_max_val = 0.9
        self._ui_label_dict = pyqt6_ui_label_dict
        self._image_path = str
        self._pyqt_img: cv2.Mat
        self.is_backup = False
        self.backup_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        assert isinstance(self.backup_time, str)
        self.screenshot_wait_time_increase: float = 1
        self.is_check_gamelog: bool = False
        self.qimg: QImage

    def _log(self):
        self._logger_time = self.get_time()
        self._logger_name = self._logger_time + \
            self._device_id.replace(":", "_")
        self._logfile_path = self.get_current_root + \
            self._device_id.replace(":", "_")

        if not self._logfile_path:
            self._logfile_path += '/'
        if not os.path.isdir(self._logfile_path + '/log'):
            os.makedirs(self._logfile_path + '/log')
        self._log_filename = self._logfile_path + '/log/' + \
            time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime()) + '.log'
        self._log_filename = self._logfile_path + '/log/' + \
            time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime()) + '.log'
        self._logger = logging.getLogger(self._logger_name)
        if not self._logger.handlers:
            self._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(levelname)-6s[%(asctime)s]:%(threadName)s: %(message)s ',
                datefmt="%H:%M:%S",
            )
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
            file_handler = logging.FileHandler(self._log_filename)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    def _send_log_to_ui(self, _log_message: str):
        if self._ui_label_dict:
            self._ui_label_dict['log_label'].setText(_log_message)

    def _send_image_path_to_ui(self, _image_path: str):
        if self._ui_label_dict:
            self._pyqt_img = cv2.imread(_image_path)
            _height, _width, _ = self._pyqt_img.shape
            _bytes_perline = 3 * _width
            self.qimg = QImage(self._pyqt_img, _width, _height, _bytes_perline,# type: ignore
                               QImage.Format.Format_RGB888).rgbSwapped()  # type: ignore
            self._ui_label_dict['image_label'].setPixmap(
                QPixmap.fromImage(self.qimg))

    def execute_time_sleep(self, wait_time: float = 0):
        self._logger.info("execute_time_sleep : wait_time= %.2f", wait_time)
        self._logger.info(
            "execute_time_sleep method : \n wait_time= %.2f", wait_time)
        time.sleep(wait_time)

    @property
    def get_current_root(self) -> str:
        return self._relatively_path

    @property
    def get_device_id(self) -> str:
        if self._device_id:
            return ' -s ' + self._device_id
        return ''

    def _check_image_name_pngFormat(self, _input_name: str) -> str:
        if '.png' in _input_name:
            return _input_name
        return _input_name + '.png'

    def _check_additional_root(self, _input_name: str) -> str:
        if _input_name:
            if _input_name[-1] != '\\' and _input_name[-1] != '/':
                return _input_name + '/'
            return _input_name
        return ''

    def _check_path(self, _path: str) -> str:
        _tmp_check_path = Path(_path)
        _tmp_check_path.mkdir(parents=True, exist_ok=True)
        return str(_path)

    def _set_screen_image_imread_cv2(self,
                                     _image_name: str = '',
                                     _screen_image_root_dict_key: str = '',
                                     _additional_root: str = '') -> None:
        self._screen_image_Mat = cv2.imread(
            f'{self.get_current_root + self.get_sub_root_path(_screen_image_root_dict_key)}{ self._check_additional_root(_additional_root)}{self._check_image_name_pngFormat(_image_name)}'
        )

    def _get_screen_image_imread_cv2(self) -> cv2.Mat:
        return self._screen_image_Mat

    def _set_template_image_imread_cv2(self,
                                       _image_name: str = '',
                                       _template_image_root_dict_key: str = '',
                                       _additional_root: str = '') -> None:
        self._template_image_Mat = cv2.imread(
            f'{self.get_current_root + self.get_sub_root_path(_template_image_root_dict_key)}{self._check_additional_root(_additional_root)}{self._check_image_name_pngFormat(_image_name)}'
        )

    def _get_template_image_imread_cv2(self) -> cv2.Mat:
        return self._template_image_Mat

    def get_sub_root_path(self, root_key: str) -> str:
        if len(self._sub_root_dict) != 0:
            return self._sub_root_dict[root_key]
        return ''

    def check_gamelog(self, params: ImageRecognitionParams):
        params.template_image_name = 'log_button'
        try:
            self._set_screen_image_imread_cv2(params.screen_image_name, params.screen_image_root_dict_key,
                                              params.screen_image_additional_root)
            self._set_template_image_imread_cv2(params.template_image_name, params.template_image_root_dict_key,
                                                params.template_image_additional_root)
            self._image_to_position(
                self._screen_image_Mat, self._template_image_Mat, params.accuracy_val)
        except Exception as e:
            self._logger.info(e)

            self.screenshot()
            self._set_screen_image_imread_cv2(params.screen_image_name, params.screen_image_root_dict_key,
                                              params.screen_image_additional_root)
            self._set_template_image_imread_cv2(params.template_image_name, params.template_image_root_dict_key,
                                                params.template_image_additional_root)
            self._image_to_position(
                self._screen_image_Mat, self._template_image_Mat, params.accuracy_val)

        if self._itp_bool:
            self._logger.info("_image_to_position method : template_name=%s prob=%.4f accuracy_val=%.4f %s",
                              params.template_image_name, self._itp_max_val, params.accuracy_val, self._itp_bool)
            self._send_image_path_to_ui(_image_path=self.get_current_root +
                                        self.get_sub_root_path(params.template_image_root_dict_key) +
                                        self._check_additional_root(params.template_image_additional_root) +
                                        self._check_image_name_pngFormat(params.template_image_name))
            self._send_log_to_ui(
                f"_image_to_position method : \n template_name={params.template_image_name}  \n prob={self._itp_max_val:.4f} \n accuracy_val={params.accuracy_val:.4f} \n {self._itp_bool}"
            )
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(
                    SaveParams(save_image_root_dict_key='backup_root',
                               save_image_name=f'{self.get_time()}_{params.template_image_name}_{self._itp_max_val:.2f}{self._itp_bool}',
                               save_image_additional_root=self.backup_time,
                               is_refresh_screenshot=False))
            self.tap(self._itp_center)

    def create_sub_root_file(self):
        """_summary_ fuction to create sub roots
        """
        for _key, _document_path in self._sub_root_dict.items():
            _document_path_temp = self.get_current_root + '/' + _document_path
            if not os.path.isdir(_document_path_temp):
                os.makedirs(_document_path_temp)

    def get_time(self) -> str:
        return time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime())

    def screenshot(
        self,
        save_screenshot_name: str = 'tmp0.png',
        save_screenshot_root_key: str = 'tmp_root',
        save_screenshot_additional_root: str = '',
    ) -> None:

        if self._os_environment == 'android':
            os.system(
                f"adb  {self.get_device_id}  shell screencap -p /sdcard/screenshot.png")
            os.system(
                f"adb  {self.get_device_id}  pull /sdcard/screenshot.png {self.get_current_root + self.get_sub_root_path(save_screenshot_root_key) +self._check_additional_root(save_screenshot_additional_root)}{self._check_image_name_pngFormat(save_screenshot_name)}"
            )
        elif self._os_environment == 'ios':
            self.wda_client.screenshot().save(  # type: ignore
                f"{self.get_current_root + self.get_sub_root_path(save_screenshot_root_key) +self._check_additional_root(save_screenshot_additional_root)}{self._check_image_name_pngFormat(save_screenshot_name)}"
            )
        else:
            raise Exception
        self._logger.debug(
            "adb_screenshot method : process %s", save_screenshot_name)
        self._send_log_to_ui(
            f"adb_screenshot method : \n process {save_screenshot_name:s}")

    def _image_to_position(self, _screen_image_Mat: Mat, _template_image_Mat: Mat, _accuracy_val: float) -> None:
        image_x, image_y = _template_image_Mat.shape[:2]
        result = cv2.matchTemplate(
            _screen_image_Mat, _template_image_Mat, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(
            result)  # type: ignore unused var

        if max_val > _accuracy_val:  # accuracy between two image
            _temp_center = (int(max_loc[0] + image_y / 2),
                            int(max_loc[1] + image_x / 2))
            self._itp_bool = True
            self._itp_center = _temp_center
            self._itp_max_val = max_val
            loc = np.where(result >= _accuracy_val)  # type: ignore
            loc_ren = len(loc[-1][:])  # type: ignore
            if loc_ren > 0:
                _temp_center_list = []
                for i in range(loc_ren):
                    # type: ignore
                    # type: ignore
                    _temp_center = (
                        int(loc[1][i] + image_y / 2), int(loc[0][i] + image_x / 2)) # type: ignore
                    _temp_center_list.append(_temp_center) # type: ignore
                    #if (): print("pos:", _temp_center)
                self._itp_center_list = _temp_center_list
        else:
            self._itp_bool = False
            self._itp_center = (0, 0)
            self._itp_max_val = max_val

    def check_image_recognition(self, params: ImageRecognitionParams) -> bool:
        save_params = SaveParams(
            save_image_root_dict_key='backup_root',
            save_image_name=f'{self.get_time()}_{params.template_image_name}_{self._itp_max_val:.2f}{self._itp_bool}',
            save_image_additional_root=self.backup_time,
            is_refresh_screenshot=False)
        if params.repeatedly_screenshot_times <= 1:
            if params.compare_times_counter > 1 and params.is_refresh_screenshot is False:
                self._logger.info('warring efficient lost')
            for _num in range(params.compare_times_counter):
                if self.is_check_gamelog:
                    self.check_gamelog(ImageRecognitionParams())
                if params.is_refresh_screenshot:
                    time.sleep(params.screenshot_wait_time +
                               self.screenshot_wait_time_increase)
                    self.screenshot(params.screen_image_name, params.screen_image_root_dict_key,
                                    params.screen_image_additional_root)
                self._set_screen_image_imread_cv2(params.screen_image_name, params.screen_image_root_dict_key,
                                                  params.screen_image_additional_root)
                self._set_template_image_imread_cv2(params.template_image_name, params.template_image_root_dict_key,
                                                    params.template_image_additional_root)
                self._image_to_position(
                    self._screen_image_Mat, self._template_image_Mat, params.accuracy_val)

                self._logger.info("_image_to_position method : template_name=%s  prob=%.4f accuracy_val=%.4f %s",
                                  params.template_image_name, self._itp_max_val, params.accuracy_val, self._itp_bool)
                self._send_image_path_to_ui(_image_path=self.get_current_root +
                                            self.get_sub_root_path(params.template_image_root_dict_key) +
                                            self._check_additional_root(params.template_image_additional_root) +
                                            self._check_image_name_pngFormat(params.template_image_name))
                self._send_log_to_ui(
                    "_image_to_position method : \n template_name={params.template_image_name}  \n prob={self._itp_max_val:.4f} \n accuracy_val={params.accuracy_val:.4f} \n {self._itp_bool}"
                )
                if self._itp_bool:
                    if self.is_backup and params.is_backup:
                        self.save_screenshot_compression(save_params)
                    return True
        else:
            _screen_image_name_list = [f'tmp{x}' for x in range(
                params.repeatedly_screenshot_times)]

            if self.is_check_gamelog:
                self.check_gamelog(ImageRecognitionParams())
            self._set_template_image_imread_cv2(params.template_image_name, params.template_image_root_dict_key,
                                                params.template_image_additional_root)
            time.sleep(params.screenshot_wait_time +
                       self.screenshot_wait_time_increase)

            for _num in range(params.compare_times_counter):
                for _temp_screen_image_name in _screen_image_name_list:

                    self.screenshot(_temp_screen_image_name, params.screen_image_root_dict_key,
                                    params.screen_image_additional_root)
                for _temp_screen_image_name in _screen_image_name_list:
                    self._set_screen_image_imread_cv2(_temp_screen_image_name, params.screen_image_root_dict_key,
                                                      params.screen_image_additional_root)
                    self._image_to_position(
                        self._screen_image_Mat, self._template_image_Mat, params.accuracy_val)
                    self._logger.info("_image_to_position method : template_name=%s  prob=%.4f accuracy_val=%.4f %s",
                                      params.template_image_name, self._itp_max_val, params.accuracy_val, self._itp_bool)
                    self._send_image_path_to_ui(_image_path=self.get_current_root +
                                                self.get_sub_root_path(params.template_image_root_dict_key) +
                                                self._check_additional_root(params.template_image_additional_root) +
                                                self._check_image_name_pngFormat(params.template_image_name))
                    self._send_log_to_ui(
                        f"_image_to_position method : \n template_name={params.template_image_name}  \n prob={self._itp_max_val:.4f} \n accuracy_val={params.accuracy_val:.4f} \n {self._itp_bool}"
                    )
                    if self._itp_bool:
                        if self.is_backup and params.is_backup:
                            self.save_screenshot_compression(save_params)
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

            if self._os_environment == 'android':
                os.system(
                    f"adb {self.get_device_id} shell input tap {_x} {_y}")
            elif self._os_environment == 'ios':
                self.wda_client.tap(int(_x / self.ios_device_scale),  # type: ignore
                                    int(_y / self.ios_device_scale))  # type: ignore
            else:
                raise Exception

            self._logger.info(
                "tap method : (x,y) = %s offset = %s", center, tap_offset)
            self._send_log_to_ui(
                f"tap method : \n (x,y) = {center} \n offset = {tap_offset}")

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

            if self._os_environment == 'android':
                os.system(
                    f"adb  {self.get_device_id} shell input swipe {_x} {_y} {_x2} {_y2} {swiping_time}")
            elif self._os_environment == 'ios':
                _ios_swipe_time = float(swiping_time) / 1000
                self.wda_client.swipe(  # type: ignore
                    int(_x / self.ios_device_scale),  # type: ignore
                    int(_y / self.ios_device_scale),  # type: ignore
                    int(_x2 / self.ios_device_scale),  # type: ignore
                    int(_y2 / self.ios_device_scale),  # type: ignore
                    _ios_swipe_time)  # type: ignore
            else:
                raise Exception

            self._logger.info("swipe method : (x,y) = %s (x2,y2) = %s swiping_time = %.2f", center, swipe_offset_position,
                              swiping_time)
            self._send_log_to_ui(
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
                self._logger.info(
                    "adb_press method : (x,y) = %s pressing_time = %d", center, pressing_time)
                self._send_log_to_ui(
                    f"adb_press method : \n (x,y) = {center} \n pressing_time = {pressing_time}")
            except Exception as e:
                self._logger.exception(f"adb_press method :  {e}")
                self._send_log_to_ui(f"adb_press method : \n {e}")

    def adb_default_tap(
            self,
            params: ImageRecognitionParams,
            tap_execute_wait_time: float = 0.1,
            tap_execute_counter_times: int = 1,
            tap_offset: Tuple[int, int] = (0, 0),
    ) -> bool:
        save_params = SaveParams(save_image_root_dict_key='backup_root',
                                 save_image_name='{}_{}_{:.2f}{}'.format(self.get_time(), params.template_image_name,
                                                                         self._itp_max_val, self._itp_bool),
                                 save_image_additional_root=self.backup_time,
                                 is_refresh_screenshot=False)
        if self.check_image_recognition(params):
            self.tap(self._itp_center, tap_execute_counter_times,
                     tap_execute_wait_time, tap_offset)
            self._logger.info("adb_default_tap method : template_name=%s  prob=%.4f %s", params.template_image_name,
                              self._itp_max_val, self._itp_bool)
            self._send_log_to_ui(
                f"adb_default_tap method : \n template_name={params.template_image_name}  \n prob={self._itp_max_val:.4f} \n {self._itp_bool}"
            )
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(save_params)
            return True

        self._logger.info("adb_default_tap method : template_name=%s  prob=%.4f %s", params.template_image_name,
                          self._itp_max_val, self._itp_bool)
        self._send_log_to_ui(
            f"adb_default_tap method : \n template_name={params.template_image_name}  \n prob={self._itp_max_val:.4f} \n {self._itp_bool}"
        )
        if self.is_backup and params.is_backup:
            self.save_screenshot_compression(save_params)
        return False

    def adb_default_swipe(
        self,
        params: ImageRecognitionParams,
        swipe_offset_position: Tuple[int, int] = (0, 0),
        swiping_time: int = 300,
        swipe_execute_counter_times: int = 1,
        swipe_execute_wait_time: float = 0,
    ) -> bool:
        save_params = SaveParams(
            save_image_root_dict_key='backup_root',
            save_image_name=f'{self.get_time()}_{params.template_image_name}_{self._itp_max_val:.2f}{self._itp_bool}',
            save_image_additional_root=self.backup_time,
            is_refresh_screenshot=False)
        # itp is accuracy between png_name and screenshot ,if > 0.9 return position else return false
        if self.check_image_recognition(params):
            self.swipe(self._itp_center, swipe_offset_position, swiping_time, swipe_execute_counter_times,
                       swipe_execute_wait_time)
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(save_params)
            return True

        if self.is_backup and params.is_backup:
            self.save_screenshot_compression(save_params)
        return False

    def adb_default_press(
        self,
        params: ImageRecognitionParams,
        pressing_time: int = 300,
        press_execute_counter_times: int = 1,
        press_execute_wait_time: float = 0,
    ) -> bool:
        save_params = SaveParams(
            save_image_root_dict_key='backup_root',
            save_image_name=f'{self.get_time()}_{params.template_image_name}_{self._itp_max_val:.2f}{self._itp_bool}',
            save_image_additional_root=self.backup_time,
            is_refresh_screenshot=False)
        if self.check_image_recognition(params):
            self.press(self._itp_center, pressing_time,
                       press_execute_counter_times, press_execute_wait_time)
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
        _img = Image.open(
            f"{self.get_current_root + self.get_sub_root_path(save_params.load_image_root_dict_key)}{self._check_image_name_pngFormat(save_params.load_image_name)}"
        )
        if save_params.is_save_image_name_add_time:
            _save_png_image_name = self.get_time() + save_params.save_image_name + '.png'
        else:
            _save_png_image_name = save_params.save_image_name + '.png'

        _image_path = self._check_path(self.get_current_root + self.get_sub_root_path(save_params.save_image_root_dict_key) +
                                       self._check_additional_root(save_params.save_image_additional_root))
        if save_params.compression != 1:
            (_w, _h) = _img.size
            #print('原始像素'+'w=%d, h=%d', w, h)
            _w = int(_w * save_params.compression)
            _h = int(_h * save_params.compression)
            _new_resize_img = _img.resize((_w, _h))
            _new_resize_img.save(_image_path + _save_png_image_name)
            if not self.is_backup:
                self._logger.info("save_screenshot_compression method : raw data w=%d, h=%d compression = %.2f name=%s ", _w,
                                  _h, save_params.compression, _save_png_image_name)
                self._send_log_to_ui(
                    f"save_screenshot_compression method :\n raw data w={_w}, h={_h}\n compression = {save_params.compression}\n name={_save_png_image_name} "
                )
        else:
            (_w, _h) = _img.size
            _img.save(_image_path + _save_png_image_name)
            if not self.is_backup:
                self._logger.info("save_screenshot_compression method : raw data w=%d, h=%d name=%s", _w, _h,
                                  _save_png_image_name)
                self._send_log_to_ui(
                    f"save_screenshot_compression method : \n raw data w={_w}, h={_h} \n name={_save_png_image_name}")

    def crop_screenshot(
        self,
        save_params: SaveParams,
        coordinate1_tuple1: Tuple[int, int],
        coordinate2_tuple2: Tuple[int, int],
    ) -> None:

        if save_params.is_refresh_screenshot:
            time.sleep(save_params.screenshot_wait_time)
            self.screenshot()
        _img = Image.open(
            f"{self.get_current_root + self.get_sub_root_path(save_params.load_image_root_dict_key)}{self._check_image_name_pngFormat(save_params.load_image_name)}"
        )
        _pos_x, _pos_y = coordinate1_tuple1
        _pos_x2, _pos_y2 = coordinate2_tuple2

        _pos_x2 -= _pos_x
        _pos_y2 -= _pos_y
        _region = (_pos_x, _pos_y, _pos_x + _pos_x2, _pos_y + _pos_y2)
        _cropImg = _img.crop(_region)
        if save_params.is_save_image_name_add_time:
            _save_png_image_name = self.get_time() + save_params.save_image_name + '.png'
        else:
            _save_png_image_name = save_params.save_image_name + '.png'
        # png_string =self.get_time()+save_name+'.png'
        _save_image_path = self._check_path(self.get_current_root +
                                            self.get_sub_root_path(save_params.save_image_root_dict_key) +
                                            self._check_additional_root(save_params.save_image_additional_root))
        _cropImg.save(_save_image_path + _save_png_image_name)
        self._logger.info(
            "crop_screenshot method : exported : w=%s", _save_png_image_name)
        self._send_log_to_ui(
            f"crop_screenshot method : \n exported : w={_save_png_image_name}")
        #print("exported:", path+png_string)

    def scan_icon_png_to_list(
        self,
        template_image_root_dict_key: str = 'icon_root',
        template_image_additional_root: str = '',
    ) -> list[str]:
        #files = listdir(path)
        _files = listdir(self.get_current_root + self.get_sub_root_path(template_image_root_dict_key) +
                         self._check_additional_root(template_image_additional_root))
        _png_file_list: list[str] = []

        for _f in _files:
            _fullpath = join(
                self.get_current_root +
                self.get_sub_root_path(
                    template_image_root_dict_key) + template_image_additional_root,
                _f)
            if isfile(_fullpath):
                if (_f[len(_f) - 1] == 'g' or _f[len(_f) - 1] == 'G') and _f[:3] != 'tmp':
                    _png_file_list.append(_f.replace('.png', ''))
            elif isdir(_fullpath):
                pass
        return natsort.natsorted(_png_file_list)

    def scan_dir_to_list(
        self,
        template_image_root_dict_key: str = 'icon_root',
        template_image_additional_root: str = '',
    ) -> list[str]:
        #files = listdir(path)
        _files = listdir(self.get_current_root + self.get_sub_root_path(template_image_root_dict_key) +
                         self._check_additional_root(template_image_additional_root))
        _png_file_list: list[str] = []

        for _f in _files:
            _fullpath = join(
                self.get_current_root + self.get_sub_root_path(template_image_root_dict_key) +
                self._check_additional_root(template_image_additional_root), _f)
            if isfile(_fullpath):
                pass
            elif isdir(_fullpath):
                _png_file_list.append(_f)
        return natsort.natsorted(_png_file_list)

    def detect_text(
        self,
        load_image_name: str = '',
        load_image_root_dict_key: str = 'tmp_root',
        load_image_additional_root: str = '',
    ) -> str:
        """Detects text in the file."""

        client = vision.ImageAnnotatorClient()
        image_file = io.open(
            "{}{}".format(
                self.get_current_root +
                self.get_sub_root_path(
                    load_image_root_dict_key) + self._check_additional_root(load_image_additional_root),
                self._check_image_name_pngFormat(load_image_name)), 'rb')
        content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)  # type: ignore
        texts = response.text_annotations  # type: ignore
        # print('Texts:')
        # print()
        if texts != []:  # type: ignore
            txt = texts[0].description  # type: ignore
            # print(txt)
            self._logger.info("detect_text method : txt = %s",
                              texts)  # type: ignore
            self._send_log_to_ui(f"detect_text method : \n txt = {texts}")
            return txt  # type: ignore

        self._logger.info("detect_text method : txt = none")
        self._send_log_to_ui(f"detect_text method : \n txt = none")
        return ""  # type: ignore

    def process_itp_center_list(self) -> list[tuple[int, int]] | None:
        if not self._itp_bool:
            return
        _temp_center_list = self._itp_center_list

        assert len(_temp_center_list) > 0

        if len(_temp_center_list) > 1:
            tmp_list = [_temp_center_list[0]]
            tmp_x, tmp_y = _temp_center_list[0]
            for i in range(1, len(_temp_center_list)):
                tmp_x2, tmp_y2 = _temp_center_list[i]
                if abs(tmp_x - tmp_x2) > 5 or abs(tmp_y - tmp_y2) > 5:
                    tmp_x, tmp_y = tmp_x2, tmp_y2
                    tmp_list.append((tmp_x, tmp_y))
            self._logger.info(
                "process_itp_center_list method : list = %s", tmp_list)
            self._send_log_to_ui(
                f"process_itp_center_list method : \n list = {tmp_list}")
            return tmp_list
        if len(_temp_center_list) == 1:
            self._logger.info(
                "process_itp_center_list method : list = %s", _temp_center_list)
            self._send_log_to_ui(
                f"process_itp_center_list method : \n list = {_temp_center_list}")
            return _temp_center_list

    def except_within_range_position(self, _center_list: list[tuple[int, int]] | None,
                                     _except_list: list[tuple[int, int]] | None, within_range_x: int,
                                     within_range_y: int) -> list[tuple[int, int]] | None:

        def do_except() -> list[tuple[int, int]] | None:
            if not _center_list:
                return _center_list
            if not _except_list:
                return _center_list

            for tmp_x, tmp_y in _center_list:
                flag = True
                for tmp_x2, tmp_y2 in _except_list:
                    if abs(tmp_x - tmp_x2) < within_range_x or abs(tmp_y - tmp_y2) < within_range_y:
                        flag = False
                        break
                if flag:
                    tmp_list.append((tmp_x, tmp_y))

        assert within_range_x >= 0
        assert within_range_y >= 0
        if _center_list == []:
            return []
        if _except_list == []:
            return _center_list
        tmp_list: list[tuple[int, int]] = []
        do_except()
        self._logger.info(
            "except_within_range_position method : list = %s", tmp_list)
        self._send_log_to_ui(
            f"except_within_range_position method : \n list = {tmp_list}")
        return tmp_list
