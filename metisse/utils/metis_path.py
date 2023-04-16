# -*- coding=UTF-8 -*-
# pyright: strict
import inspect
import os
from ..settings import Settings as ST
from pathlib import Path
from typing import Any
from ..params import ImageRecognitionParams, SaveParams


class DevPath(object):
    """
    setup dev environment
    """

    def __init__(self, current_path: str) -> None:
        self._absolute_path = os.path.abspath(current_path)
        self.initialize_dev_environment()

    def initialize_dev_environment(self) -> None:
        """
        generate dev root path (icon , ui ) files
        """
        for _document_path in ST.DEV_ENVIRONMENT_ROOT_PATH:
            _document_path_temp = os.path.join(self._absolute_path, _document_path)
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
        self.absolute_path = current_path
        self.device_id_path = os.path.abspath(os.path.join(
            current_path, device_id))  # specific device id path (init script auto generate device id file)
        self.device_id = device_id
        self.initialize_script_environment()

    def initialize_script_environment(self) -> None:
        """
        generate script root path (temp_image,storage,backup,log ) files
        """
        for _document_path in ST.SCRIPT_ENVIRONMENT_ROOT_PATH:
            _document_path_temp = os.path.join(self.device_id_path, _document_path)
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
        _path = os.path.join(_path, device_id)
        script_path = ScriptPath(device_id, _path)
        script_path.initialize_script_environment()
        return script_path

    def _check_image_name_pngFormat(self, _input_name: str) -> str:
        if '.png' in _input_name:
            return _input_name
        return _input_name + '.png'

    def check_path(self, _path: str) -> str:
        _tmp_check_path = Path(_path)
        _tmp_check_path.mkdir(parents=True, exist_ok=True)
        return str(_path)

    def get_image_path(self, _image_name: str = '', _image_root: str = '', _additional_root: str = '') -> str:
        _image_name = self._check_image_name_pngFormat(_image_name)
        self._screen_image_path = os.path.join(self.device_id_path, _image_root, _additional_root, _image_name)
        return self._screen_image_path

    def get_screen_image_path(self, path_params: ImageRecognitionParams) -> str:
        _image_name = self._check_image_name_pngFormat(path_params.screen_image_name)
        _subdirs = ''
        if path_params.screen_image_subdirs:
            _subdirs = os.path.join(*path_params.screen_image_subdirs)
        self._screen_image_path = os.path.join(self.device_id_path, path_params.screen_image_primary_dir,
                                               path_params.screen_image_secondary_dir, _subdirs, _image_name)
        return self._screen_image_path

    def get_template_image_path(self, path_params: ImageRecognitionParams) -> str:
        _image_name = self._check_image_name_pngFormat(path_params.template_image_name)
        _subdirs = ''
        if path_params.template_image_subdirs:
            _subdirs = os.path.join(*path_params.template_image_subdirs)
        if path_params.template_image_primary_dir == 'temp_image':  # temp_image default in the device folder , adjust path
            self._screen_image_path = os.path.join(self.device_id_path, path_params.template_image_primary_dir,
                                                   path_params.template_image_secondary_dir, _subdirs, _image_name)
        else:
            self._screen_image_path = os.path.join(self.absolute_path, path_params.template_image_primary_dir,
                                                   path_params.template_image_secondary_dir, _subdirs, _image_name)

        return self._screen_image_path

    def get_load_image_path(self, path_params: SaveParams) -> str:
        _image_name = self._check_image_name_pngFormat(path_params.load_image_name)
        _subdirs = ''
        if path_params.load_image_subdirs:
            _subdirs = os.path.join(*path_params.load_image_subdirs)
        self._screen_image_path = os.path.join(self.device_id_path, path_params.load_image_primary_dir,
                                               path_params.load_image_secondary_dir, _subdirs, _image_name)
        return self._screen_image_path

    def get_save_image_path(self, path_params: SaveParams) -> str:
        _image_name = self._check_image_name_pngFormat(path_params.save_image_name)
        _subdirs = ''
        if path_params.save_image_subdirs:
            _subdirs = os.path.join(*path_params.save_image_subdirs)

        self._screen_image_path = os.path.join(self.device_id_path, path_params.save_image_primary_dir,
                                               path_params.save_image_secondary_dir, _subdirs, _image_name)

        return self._screen_image_path