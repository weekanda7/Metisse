# -*- coding=UTF-8 -*-
# pyright: strict
import inspect
import os
from ..settings import Settings as ST
from pathlib import Path
from typing import Any
from ..params import  ImageRecognitionParams
class DevPath(object):
    """
    setup dev environment
    """
    def __init__(self,current_path: str) -> None:
        self._absolute_path = os.path.abspath(current_path)
        if os.path.exists(self._absolute_path):
            print("Path exists:", self._absolute_path)
        else:
            print("Path does not exist:", self._absolute_path)

    def initialize_dev_environment(self) -> None:
        """
        generate dev root path (icon , script , ui , log ) files
        """
        for  _document_path in ST.DEV_ENVIRONMENT_ROOT_PATH:
            _document_path_temp = os.path.join(self._absolute_path,_document_path)
            if not os.path.isdir(_document_path_temp):
                os.makedirs(_document_path_temp)
    @staticmethod
    def auto_generate_dev_path():
        """
        auto generate dev root path
        """
        caller_frame = inspect.stack()[1]  # 获取调用栈的上一级帧
        caller_file_path = caller_frame.filename  # 获取调用该方法的文件路径

        _path = os.path.dirname(os.path.abspath(caller_file_path))
        _path = os.path.join(_path, ".")
        dev_path = DevPath(_path)
        dev_path.initialize_dev_environment()
    def create_extended_script_path(self, device_id: str) -> 'ScriptPath':
        """
        Create an ExtendedDevPath object that inherits from DevPath and has new attributes and methods.

        Args:
            new_attribute (str): The new attribute to be added to the ExtendedDevPath object.

        Returns:
            ExtendedDevPath: An instance of the ExtendedDevPath class.
        """
        return ScriptPath(self._absolute_path, device_id)

class ScriptPath(DevPath):
    """
    This class inherits from DevPath and adds new features.
    """

    def __init__(self, current_path: str, device_id: str) -> None:
        super().__init__(current_path)
        self.absolute_path_without =current_path
        self.absolute_path = os.path.abspath(os.path.join(current_path,device_id))
        if os.path.exists(self.absolute_path):
            print("Path exists:", self.absolute_path)
        else:
            print("Path does not exist:", self.absolute_path)
        self.device_id = device_id

    def initialize_script_environment(self) -> None:
        """
        generate script root path (temp_image,storage,backup ) files
        """
        for _document_path in ST.SCRIPT_ENVIRONMENT_ROOT_PATH:
            _document_path_temp = os.path.join(self.absolute_path, _document_path)
            if not os.path.isdir(_document_path_temp):
                os.makedirs(_document_path_temp)

    @staticmethod
    def auto_generate_script_path(device_id: str) -> object:
        """
        auto generate script root path
        """
        caller_frame = inspect.stack()[1]  # 获取调用栈的上一级帧
        caller_file_path = caller_frame.filename  # 获取调用该方法的文件路径

        _path = os.path.dirname(os.path.abspath(caller_file_path))
        _path = os.path.join(_path, ".")
        script_path = ScriptPath(device_id, _path)
        script_path.initialize_script_environment()
        return script_path

    def _check_image_name_pngFormat(self, _input_name: str) -> str:
        if '.png' in _input_name:
            return _input_name
        return _input_name + '.png'

    def _check_path(self, _path: str) -> str:
        _tmp_check_path = Path(_path)
        _tmp_check_path.mkdir(parents=True, exist_ok=True)
        return str(_path)

    def get_image_path(self, _image_name: str = '', _image_root: str = '', _additional_root: str = '') -> str:
        _image_name = self._check_image_name_pngFormat(_image_name)
        self._screen_image_path = os.path.join(self.absolute_path, _image_root, _additional_root, _image_name)
        return self._screen_image_path
    def get_image_path_without_id(self, _image_name: str = '', _image_root: str = '', _additional_root: str = '') -> str:
        _image_name = self._check_image_name_pngFormat(_image_name)
        self._screen_image_path = os.path.join(self.absolute_path_without, _image_root, _additional_root, _image_name)
        return self._screen_image_path
    def get_screen_image_path(self, path_params:ImageRecognitionParams) -> str:
        _image_name = self._check_image_name_pngFormat(path_params.screen_image_name)
        self._screen_image_path = os.path.join(self.absolute_path, path_params.screen_image_root_name, path_params.screen_image_additional_root_name, _image_name)
        return self._screen_image_path
    def get_template_image_path(self, path_params:ImageRecognitionParams) -> str:
        _image_name = self._check_image_name_pngFormat(path_params.template_image_name)
        self._screen_image_path = os.path.join(self.absolute_path_without, path_params.template_image_root_name, path_params.template_image_additional_root_name, _image_name)
        return self._screen_image_path
