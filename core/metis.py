# -*- coding=UTF-8 -*-
# pyright: strict
"""
This module contains functions for android and ios script.
It includes device port connect, screen shoot ,image similarity calculation, device control.
"""

from __future__ import annotations
import io
import logging
import os
import time
try:
    import wda  # type: ignore
except ImportError:
    print('No module')
from os import listdir
from os.path import isdir, isfile, join
from typing import Tuple
# pylint: disable=no-member
from PIL import Image
import natsort
from google.cloud import vision  # type: ignore
from .params import ImageRecognitionParams, SaveParams, DeviceParams, UiClientParams, ImageRecognitionResult
from .template_metis import TemplateMetisClass
from .clients.ios.wda import WdaClient
from .clients.andriod.adb import AdbClient
from .utils.metis_path import DevPath
from .utils.opencv_utils import Opencv_utils
from .utils.ui_client import UiClient
from .utils.metis_log import MetisLogger
from .utils import image_recognition
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fine_key.json'

OS_ENVIRONMENT = ['android', 'ios']


class MetisClass(TemplateMetisClass):

    def __init__(self,
                 device_id: str,
                 relatively_path: str,
                 pyqt6_ui_label_dict: UiClientParams,
                 os_environment: str = 'android'):
        self._relatively_path = relatively_path

        super(TemplateMetisClass, self).__init__()

        self._device_id = device_id
        self._dev_path = DevPath(relatively_path)
        self._script_path = self._dev_path.create_extended_script_path(self._device_id)
        self._logger = MetisLogger("MetisClass_logger", log_level=logging.DEBUG, log_file=os.path.join(self._script_path.absolute_path , "log" , self._device_id + ".log"))
        assert os_environment in OS_ENVIRONMENT
        self._os_environment = os_environment  # android , ios
        self.ios_device_scale = 2  # init var

        if self._os_environment == 'ios':
            self._client = WdaClient(DeviceParams(device_id, os_environment))
        elif self._os_environment == 'android':
            self._client = AdbClient(DeviceParams(device_id, os_environment))
        else:
            raise ValueError('os_environment must be android or ios')

        self._img_recog_result =ImageRecognitionResult()

        self._ui_client = UiClient(pyqt6_ui_label_dict)

        self.is_backup = False
        self.backup_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        assert isinstance(self.backup_time, str)
        self.screenshot_wait_time_increase: float = 1
        self.is_check_gamelog: bool = False

    def execute_time_sleep(self, wait_time: float = 0):
        self._logger.info("execute_time_sleep : wait_time= %.2f", wait_time)
        self._logger.info("execute_time_sleep method : \n wait_time= %.2f", wait_time)
        time.sleep(wait_time)

    @property
    def get_device_id(self) -> str:
        if self._device_id:
            return ' -s ' + self._device_id
        return ''

    def check_gamelog(self, params: ImageRecognitionParams):
        params.template_image_name = 'log_button'
        try:
            _screen_image_path = self._script_path.get_screen_image_path(params)
            _template_image_path = self._script_path.get_template_image_path(params)
            self.opencv_utils = Opencv_utils(_screen_image_path, _template_image_path)
            self._img_recog_result=image_recognition.match_template(self.opencv_utils.screen_image_mat, self.opencv_utils.template_image_mat,
                                    params.accuracy_val)
        except FileNotFoundError as error_msg:
            self._logger.info("FileNotFoundError: %s", error_msg)
        except ValueError as error_msg:
            self._logger.info("ValueError: %s", error_msg)
            self.screenshot()
            _screen_image_path = self._script_path.get_screen_image_path(params)
            _template_image_path = self._script_path.get_template_image_path(params)
            self.opencv_utils = Opencv_utils(_screen_image_path, _template_image_path)
            self._img_recog_result=image_recognition.match_template(self.opencv_utils.screen_image_mat, self.opencv_utils.template_image_mat,
                                    params.accuracy_val)

        if self._img_recog_result.is_recognized:
            self._logger.info("match_template method : template_name=%s prob=%.4f accuracy_val=%.4f %s",
                              params.template_image_name, self._img_recog_result.recognition_threshold, params.accuracy_val, self._img_recog_result.is_recognized)
            self._ui_client.send_image_path_to_ui(_image_path=_template_image_path)
            self._ui_client.send_log_to_ui(
                f"match_template method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n accuracy_val={params.accuracy_val:.4f} \n {self._img_recog_result.is_recognized}"
            )
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(
                    SaveParams(save_image_root_name='backup_root',
                               save_image_name=
                               f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
                               save_image_additional_root_name=self.backup_time,
                               is_refresh_screenshot=False))
            self.tap(self._img_recog_result.coordinate)

    def get_time(self) -> str:
        return time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime())

    def screenshot(
        self,
        save_screenshot_name: str = 'tmp0.png',
        save_screenshot_root_key: str = 'tmp_root',
        save_screenshot_additional_root: str = '',
    ) -> None:

        if self._os_environment == 'android':

            self._client.screenshot(
                f"adb  {self.get_device_id}  pull /sdcard/screenshot.png {self._script_path.get_image_path(save_screenshot_name,save_screenshot_root_key,save_screenshot_additional_root)}"
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
            save_image_root_name='backup_root',
            save_image_name=f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
            save_image_additional_root_name=self.backup_time,
            is_refresh_screenshot=False)

        def _single_time() -> bool:
            if params.compare_times_counter > 1 and params.is_refresh_screenshot is False:
                self._logger.info('warring efficient lost')
            for _num in range(params.compare_times_counter):
                if self.is_check_gamelog:
                    self.check_gamelog(ImageRecognitionParams())
                if params.is_refresh_screenshot:
                    time.sleep(params.screenshot_wait_time + self.screenshot_wait_time_increase)
                    self.screenshot(params.screen_image_name, params.screen_image_root_name,
                                    params.screen_image_additional_root_name)

                _screen_image_path = self._script_path.get_screen_image_path(params)
                _template_image_path = self._script_path.get_template_image_path(params)
                self.opencv_utils = Opencv_utils(_screen_image_path, _template_image_path)
                self._img_recog_result=image_recognition.match_template(self.opencv_utils.screen_image_mat, self.opencv_utils.template_image_mat,
                                        params.accuracy_val)

                self._logger.info("image_recognition method : template_name=%s  prob=%.4f accuracy_val=%.4f %s",
                                  params.template_image_name, self._img_recog_result.recognition_threshold, params.accuracy_val, self._img_recog_result.is_recognized)
                self._ui_client.send_image_path_to_ui(_image_path=_template_image_path)
                self._ui_client.send_log_to_ui(
                    "image_recognition method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n accuracy_val={params.accuracy_val:.4f} \n {self._img_recog_result.is_recognized}"
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

                    self.screenshot(_temp_screen_image_name, params.screen_image_root_name,
                                    params.screen_image_additional_root_name)
                for _temp_screen_image_name in _screen_image_name_list:
                    _screen_image_path = self._script_path.get_screen_image_path(params)

                    self.opencv_utils = Opencv_utils(_screen_image_path, _template_image_path)
                    self._img_recog_result=image_recognition.match_template(self.opencv_utils.screen_image_mat, self.opencv_utils.template_image_mat,
                                            params.accuracy_val)
                    self._logger.info("match_template method : template_name=%s  prob=%.4f accuracy_val=%.4f %s",
                                      params.template_image_name, self._img_recog_result.recognition_threshold, params.accuracy_val, self._img_recog_result.is_recognized)
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

    def adb_default_tap(
            self,
            params: ImageRecognitionParams,
            tap_execute_wait_time: float = 0.1,
            tap_execute_counter_times: int = 1,
            tap_offset: Tuple[int, int] = (0, 0),
    ) -> bool:
        save_params = SaveParams(
            save_image_root_name='backup_root',
            save_image_name=f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
            save_image_additional_root_name=self.backup_time,
            is_refresh_screenshot=False)
        if self.check_image_recognition(params):
            self.tap(self._img_recog_result.coordinate, tap_execute_counter_times, tap_execute_wait_time, tap_offset)
            self._logger.info("adb_default_tap method : template_name=%s  prob=%.4f %s", params.template_image_name,
                              self._img_recog_result.recognition_threshold, self._img_recog_result.is_recognized)
            self._ui_client.send_log_to_ui(
                f"adb_default_tap method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n {self._img_recog_result.is_recognized}"
            )
            if self.is_backup and params.is_backup:
                self.save_screenshot_compression(save_params)
            return True

        self._logger.info("adb_default_tap method : template_name=%s  prob=%.4f %s", params.template_image_name,
                          self._img_recog_result.recognition_threshold, self._img_recog_result.is_recognized)
        self._ui_client.send_log_to_ui(
            f"adb_default_tap method : \n template_name={params.template_image_name}  \n prob={self._img_recog_result.recognition_threshold:.4f} \n {self._img_recog_result.is_recognized}"
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
            save_image_root_name='backup_root',
            save_image_name=f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
            save_image_additional_root_name=self.backup_time,
            is_refresh_screenshot=False)
        # itp is accuracy between png_name and screenshot ,if > 0.9 return position else return false
        if self.check_image_recognition(params):
            self.swipe(self._img_recog_result.coordinate, swipe_offset_position, swiping_time, swipe_execute_counter_times,
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
            save_image_root_name='backup_root',
            save_image_name=f'{self.get_time()}_{params.template_image_name}_{self._img_recog_result.recognition_threshold:.2f}{self._img_recog_result.is_recognized}',
            save_image_additional_root_name=self.backup_time,
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
        _img = Image.open(self._script_path.get_image_path(save_params.load_image_name, save_params.load_image_root_name))
        if save_params.is_save_image_name_add_time:
            _save_png_image_name = self.get_time() + save_params.save_image_name + '.png'
        else:
            _save_png_image_name = save_params.save_image_name + '.png'

        _image_path = self._script_path.get_image_path(_save_png_image_name, save_params.save_image_root_name)
        if save_params.compression != 1:
            (_w, _h) = _img.size
            #print('原始像素'+'w=%d, h=%d', w, h)
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
        save_params: SaveParams,
        coordinate1_tuple1: Tuple[int, int],
        coordinate2_tuple2: Tuple[int, int],
    ) -> None:

        if save_params.is_refresh_screenshot:
            time.sleep(save_params.screenshot_wait_time)
            self.screenshot()
        _img = Image.open(self._script_path.get_image_path(save_params.load_image_name, save_params.load_image_root_name))
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
        # png_string =self.get_time()+save_name+'.png'

        _crop_img.save(
            self._script_path.get_image_path(_save_png_image_name, save_params.save_image_root_name,
                                             save_params.save_image_additional_root_name))
        self._logger.info("crop_screenshot method : exported : w=%s", _save_png_image_name)
        self._ui_client.send_log_to_ui(f"crop_screenshot method : \n exported : w={_save_png_image_name}")
        #print("exported:", path+png_string)

    def scan_icon_png_to_list(
        self,
        template_image_root_name: str = 'icon_root',
        template_image_additional_root_name: str = '',
    ) -> list[str]:
        #files = listdir(path)

        _files = listdir(
            self._script_path.get_image_path(_image_name='',
                                             _image_root=template_image_root_name,
                                             _additional_root=template_image_additional_root_name))
        _png_file_list: list[str] = []

        for _f in _files:
            _fullpath = join(
                self._script_path.get_image_path(_image_name='',
                                                 _image_root=template_image_root_name,
                                                 _additional_root=template_image_additional_root_name), _f)
            if isfile(_fullpath):
                if (_f[len(_f) - 1] == 'g' or _f[len(_f) - 1] == 'G') and _f[:3] != 'tmp':
                    _png_file_list.append(_f.replace('.png', ''))
            elif isdir(_fullpath):
                pass
        return natsort.natsorted(_png_file_list)

    def scan_dir_to_list(
        self,
        template_image_root_name: str = 'icon_root',
        template_image_additional_root_name: str = '',
    ) -> list[str]:
        #files = listdir(path)
        _files = listdir(
            self._script_path.get_image_path(_image_name='',
                                             _image_root=template_image_root_name,
                                             _additional_root=template_image_additional_root_name))
        _png_file_list: list[str] = []

        for _f in _files:
            _fullpath = join(
                self._script_path.get_image_path(_image_name='',
                                                 _image_root=template_image_root_name,
                                                 _additional_root=template_image_additional_root_name), _f)
            if isfile(_fullpath):
                pass
            elif isdir(_fullpath):
                _png_file_list.append(_f)
        return natsort.natsorted(_png_file_list)

    def detect_text(
        self,
        load_image_name: str = '',
        load_image_root_name: str = 'tmp_root',
        load_image_additional_root: str = '',
    ) -> str:
        """Detects text in the file."""

        client = vision.ImageAnnotatorClient()

        file_path = f"{self._script_path.get_image_path(load_image_name,load_image_root_name,load_image_additional_root)}"
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)  # type: ignore
        texts = response.text_annotations  # type: ignore
        # print('Texts:')
        # print()
        if texts != []:  # type: ignore
            txt = texts[0].description  # type: ignore
            # print(txt)
            self._logger.info("detect_text method : txt = %s", texts)  # type: ignore
            self._ui_client.send_log_to_ui(f"detect_text method : \n txt = {texts}")
            return txt  # type: ignore

        self._logger.info("detect_text method : txt = none")
        self._ui_client.send_log_to_ui("detect_text method : \n txt = none")
        return ""  # type: ignore

    def process_itp_center_list(self) -> list[tuple[int, int]] | None:
        if not self._img_recog_result.is_recognized:
            return None
        _temp_center_list = self._img_recog_result.coordinates_list

        assert len(_temp_center_list) > 0

        if len(_temp_center_list) > 1:
            tmp_list = [_temp_center_list[0]]
            tmp_x, tmp_y = _temp_center_list[0]
            for i in range(1, len(_temp_center_list)):
                tmp_x2, tmp_y2 = _temp_center_list[i]
                if abs(tmp_x - tmp_x2) > 5 or abs(tmp_y - tmp_y2) > 5:
                    tmp_x, tmp_y = tmp_x2, tmp_y2
                    tmp_list.append((tmp_x, tmp_y))
            self._logger.info("process_itp_center_list method : list = %s", tmp_list)
            self._ui_client.send_log_to_ui(f"process_itp_center_list method : \n list = {tmp_list}")
            return tmp_list
        if len(_temp_center_list) == 1:
            self._logger.info("process_itp_center_list method : list = %s", _temp_center_list)
            self._ui_client.send_log_to_ui(f"process_itp_center_list method : \n list = {_temp_center_list}")
            return _temp_center_list
        return None

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
            return None

        assert within_range_x >= 0
        assert within_range_y >= 0
        if _center_list == []:
            return None
        if _except_list == []:
            return _center_list
        tmp_list: list[tuple[int, int]] = []
        do_except()
        self._logger.info("except_within_range_position method : list = %s", tmp_list)
        self._ui_client.send_log_to_ui(f"except_within_range_position method : \n list = {tmp_list}")
        return tmp_list