# -*- coding=UTF-8 -*-
# pyright: strict
import importlib
import os
import sys
import time
from dataclasses import dataclass
import cv2
import ctypes
from typing import Any, Dict, List
from multiprocessing import Pool
import threading
import dill  # type: ignore
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QImage, QPixmap
from gui_settings import UiSettings as UI_ST

curPath = os.path.abspath(os.path.dirname(__file__))

@dataclass
class UiClientParams:
    image_label: QtWidgets.QLabel = None  # type: ignore
    log_label: QtWidgets.QLabel = None  # type: ignore

class MainWindow(QMainWindow):

    def __init__(self, *args: Any, **kwargs: Any):


        self.lang_list = ['_tc', '_sc', '_jp', '_en', '_kr']
        directory = os.path.dirname(curPath)  #upper level directory
        self.loaded_scripts = self.load_scripts_from_directory(directory)
        self.script_list = []
        # dynamic import script
        for script_name, _ in self.loaded_scripts.items():
            print(f"load script: {script_name}")
            self.script_list.append(script_name)

        super(MainWindow, self).__init__(*args, **kwargs)
        self.setup_ui()
        self.current_select_device_name: str
        self.current_select_device_id: str
        self.current_select_device_envi: str
        self.current_select_lang: str
        self.current_select_script: str
        self.sub_obj_dict = {str: Dialog}

    def load_scripts_from_directory(self, directory: str, script_prefix: str = "script"):
        scripts = {}

        for file in os.listdir(directory):
            if file.startswith(script_prefix) and file.endswith(".py"):
                script_name = file[:-3]
                script_path = os.path.join(directory, file)

                spec = importlib.util.spec_from_file_location(script_name, script_path)
                script_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(script_module)

                scripts[script_name] = script_module

        return scripts

    def setup_ui(self):
        #Load the UI Page by PyQt6
        uic.loadUi(os.path.join(curPath, UI_ST.LOAD_MAIN_UI), self)  # type: ignore
        self.setWindowTitle(UI_ST.LOAD_MAIN_UI)
        self.set_listWidget()

        # signal
        self.script_listWidget.currentItemChanged.connect(self.set_info)
        self.lang_listWidget.currentItemChanged.connect(self.set_info)
        self.device_listWidget.currentItemChanged.connect(self.set_info)

        self.excute_button.clicked.connect(self.sub_ui)
        self.renew_button.clicked.connect(self.renew)
        self.sub2_button.clicked.connect(self.sub2_ui)
        self.sub3_button.clicked.connect(self.sub3_ui)

    def set_listWidget(self):
        self.devices_dict: dict[str, list[str]] = {}
        _list_devices: Dict[str, List[str]] = {}
        _list_devices.update(self.readDevicesList_ios())
        _list_devices.update(self.readDevicesList_andriod())
        for _i_key, _i_value in _list_devices.items():
            _RealDeviceName = _i_key
            self.devices_dict[_RealDeviceName] = _i_value
            self.device_listWidget.addItem(_RealDeviceName)
        for _i in range(len(self.lang_list)):
            self.lang_listWidget.addItem(self.lang_list[_i])
        for _i in range(len(self.script_list)):
            self.script_listWidget.addItem(self.script_list[_i])

    def set_info(self):
        try:
            self.script_listWidget.currentItem().text()
            self.current_select_script = self.script_listWidget.currentItem().text()
        except Exception as _e:
            print(_e)
            self.current_select_script = ''
        try:
            self.lang_listWidget.currentItem().text()
            self.current_select_lang = self.lang_listWidget.currentItem().text()
        except Exception as _e:
            print(_e)
            self.current_select_lang = '_tw'
        try:

            self.current_select_device_name = self.device_listWidget.currentItem().text()
            self.current_select_device_id = self.devices_dict[self.current_select_device_name][0]
            self.current_select_device_envi = self.devices_dict[self.current_select_device_name][1]
        except Exception as _e:
            print(_e)
            self.current_select_device_name = ''
            self.current_select_device_id = ''
            self.current_select_device_envi = ''
        self.text_label_show_info.setText('目前腳本: {}   語言: {} \n目前裝置: {} \n裝置 sid : {} \n裝置環境: {}'.format(
            self.current_select_script,
            self.current_select_lang,
            self.current_select_device_name,
            self.current_select_device_id,
            self.current_select_device_envi,
        ))

    def readDevicesList_ios(self) -> Dict[str, List[str]]:
        devicesNames_dict: Dict[str, List[str]] = {}
        try:
            p = os.popen('tidevice list')
            devicesList = p.read()
            p.close()
            if devicesList == '': raise Exception('please check tidevice !')
            info_lists = devicesList.split("\n")
            for info_row_str in info_lists:
                info_row_list = list(filter(None, info_row_str.split('  ')))
                if info_row_list and info_row_list[0] != 'UDID':
                    if info_row_list[2] in devicesNames_dict:
                        print('ios device name existed !')
                    devicesNames_dict[info_row_list[2]] = [info_row_list[0], 'ios']
        except Exception as e:
            print(e)
        return devicesNames_dict

    def readDevicesList_andriod(self) -> Dict[str, List[str]]:
        _p = os.popen('adb devices')
        _devices_list = _p.read()
        _p.close()
        _lists = _devices_list.split("\n")
        _devices_name_list: Dict[str, List[str]] = {}

        for _item in _lists:
            if (_item.strip() == ""):
                continue
            elif (_item.startswith("List of")):
                continue
            else:
                _devices_name_list[self.getRealDeviceName_android(_item.split("\t")[0])] = [_item.split("\t")[0], 'android']

        return _devices_name_list

    def getRealDeviceName_android(self, _deviceid: str):
        p = os.popen('adb -s ' + _deviceid + ' shell getprop ro.product.manufacturer')
        manufacturer = p.read()
        p.close()
        p = os.popen('adb -s ' + _deviceid + ' shell getprop ro.product.model')
        model = p.read()
        p.close()
        return manufacturer.strip() + " " + model.strip()

    # slot
    def sub_ui(self) -> None:

        self.set_info()

        pk = dill.dumps(self.create_small_window())  # type: ignore
        new_obj = dill.loads(pk)  # type: ignore
        pool = Pool(processes=2)
        pool_outputs = pool.map(new_obj, [])  # type: ignore
        pool.close()
        #pool.join() #debug
        time.sleep(1)

    def create_small_window(self):

        self.sub_obj_dict[self.current_select_device_name] = Dialog(  # type: ignore
            select_device_name=self.current_select_device_name,
            select_device_id=self.current_select_device_id,
            select_lang=self.current_select_lang,
            select_script=self.current_select_script,
            select_device_envi=self.current_select_device_envi,
            script_list=self.script_list,
            loaded_scripts=self.loaded_scripts,
        )  # type: ignore
        self.sub_obj_dict[self.current_select_device_name].thread_t1()  # type: ignore

    def get_select_device(self) -> str:
        try:
            _select_currentItem = self.device_listWidget.currentItem().text()
            self.text_label_show_info.setText('目前選擇裝置: ' + _select_currentItem)
            return _select_currentItem
        except Exception as _e:
            print(_e)
            self.text_label_show_info.setText('未選擇裝置')
            return ''

    def renew(self) -> None:
        self.device_listWidget.clear()
        self.lang_listWidget.clear()
        self.script_listWidget.clear()
        self.set_listWidget()

    def sub2_ui(self) -> None:
        self.set_info()
        self.sub2 = Dialog2(
            select_device_name=self.current_select_device_name,
            select_device_id=self.current_select_device_id,
            select_device_envi=self.current_select_device_envi,
        )

    def sub3_ui(self) -> None:
        self.sub3 = Dialog3(select_script=self.current_select_script)


class Dialog(QtWidgets.QDialog):

    def __init__(self,
                 select_device_name: str = '',
                 select_device_id: str = '',
                 select_lang: str = '',
                 select_script: str = '',
                 select_device_envi: str = '',
                 script_list: List[str] = [],
                 loaded_scripts=None,
                 *args: Any,
                 **kwargs: Any):
        super(Dialog, self).__init__(*args, **kwargs)
        uic.loadUi(os.path.join(curPath, UI_ST.LOAD_SUB_UI[0]), self)  # type: ignore
        self.setWindowTitle(UI_ST.LOAD_SUB_UI[0])
        # signal
        self.script_list = script_list
        self.loaded_scripts = loaded_scripts
        self.stop_Button.clicked.connect(self.stop)
        self.select_device_name = select_device_name
        self.select_device_id = select_device_id
        self.select_lang = select_lang
        self.select_script = select_script
        self.select_device_envi = select_device_envi
        self.info_label.setText('目前腳本: {}   語言: {} \n目前裝置: {} \n裝置 sid : {} \n裝置環境: {}'.format(
            self.select_script,
            self.select_lang,
            self.select_device_name,
            self.select_device_id,
            self.select_device_envi,
        ))
        self.flag_end = True
        self.log_label.setText('')
        self.image_label.setText('')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)  # type: ignore
        self.startDate = QDateTime.currentMSecsSinceEpoch()
        self.timer.start()

        self.t1: threading.Thread
        self.show()

    # slot
    def stop(self) -> None:
        self.close()
        ctypes.pythonapi.PyThreadState_SetAsyncExc(self.t1.native_id, ctypes.py_object(SystemExit))

    def closeEvent(self, a0):
        self.close()
        ctypes.pythonapi.PyThreadState_SetAsyncExc(self.t1.native_id, ctypes.py_object(SystemExit))

    def set_text(self):
        self.record_label.setText('錄影剩餘時間')
        self.startDate = QDateTime.currentMSecsSinceEpoch()

    def refresh(self):
        if self.flag_end:
            self.nowDate = QDateTime.currentMSecsSinceEpoch()
            interval = self.nowDate - self.startDate
            if interval > 0:
                days = interval // (24 * 60 * 60 * 1000)
                hour = (interval - days * 24 * 60 * 60 * 1000) // (60 * 60 * 1000)
                min = (interval - days * 24 * 60 * 60 * 1000 - hour * 60 * 60 * 1000) // (60 * 1000)
                sec = (interval - days * 24 * 60 * 60 * 1000 - hour * 60 * 60 * 1000 - min * 60 * 1000) // 1000
                intervals = str(min) + ':' + str(sec)
                self.lcdNumber.display(intervals)
        else:
            self.destroy()

    def thread_t1(self):
        self.t1 = threading.Thread(
            name=self.select_device_id,
            target=self.execute_select_script,  # type: ignore
            args=[])  #build thread

        self.t1.daemon = True
        self.t1.start()  #執行

    def execute_select_script(self):
        # com.pinkcore.heros
        _temp_args = {
            'device_id': self.select_device_id,
            'relatively_path': None,
            'pyqt6_ui_label': UiClientParams(image_label=self.image_label , log_label=self.log_label),
            'os_environment': self.select_device_envi,
        }

        script_module = self.loaded_scripts[self.select_script]
        script_instance = getattr(script_module, self.select_script)(**_temp_args)
        script_instance(self.select_lang)

        self.flag_end = False


class Dialog2(QtWidgets.QDialog):

    def __init__(self,
                 select_device_name: str = '',
                 select_device_id: str = '',
                 select_device_envi: str = '',
                 *args: Any,
                 **kwargs: Any):
        super(Dialog2, self).__init__(*args, **kwargs)

        self.select_device_name = select_device_name
        self.select_device_id = select_device_id
        self.select_device_envi = select_device_envi

        self.setup_ui()
        self.show()

    def setup_ui(self):
        uic.loadUi(os.path.join(curPath, UI_ST.LOAD_SUB_UI[1]), self)  # type: ignore
        self.setWindowTitle(UI_ST.LOAD_SUB_UI[1])
        #153
        list_screen_size = UI_ST.DEVICE_SCREEN_SIZE
        list_screen_dpi = UI_ST.DEVICE_SCREEN_DENSITY
        for screen_size in list_screen_size:
            self.size_listWidget.addItem(screen_size)
        for screen_dpi in list_screen_dpi:
            self.dpi_listWidget.addItem(screen_dpi)
        self.screen_size = '1280x720'
        self.screen_dpi = '160'
        # slot

        self.info_label.setText('目前裝置: {} \n裝置 sid : {} \n裝置環境: {}\n解析度: {}dpi: {}'.format(
            self.select_device_name,
            self.select_device_id,
            self.select_device_envi,
            self.get_device_size(),
            self.get_device_dpi(),
        ))
        self.size_listWidget.currentItemChanged.connect(self.set_screen_size)
        self.dpi_listWidget.currentItemChanged.connect(self.set_screen_dpi)
        self.stop_Button.clicked.connect(self.stop)
        self.adjust_button.clicked.connect(
            lambda: os.system("adb -s {} shell wm size {}".format(self.select_device_id, self.screen_size)))
        self.reset_button.clicked.connect(lambda: os.system("adb -s {} shell wm size reset".format(self.select_device_id)))
        self.dpi_adjust_button.clicked.connect(
            lambda: os.system("adb -s {} shell wm density {}".format(self.select_device_id, self.screen_dpi)))
        self.dpi_reset_button.clicked.connect(
            lambda: os.system("adb -s {} shell wm density reset".format(self.select_device_id)))
        self.adb_button.clicked.connect(lambda: os.system("adb devices"))
        self.adb_kill_button.clicked.connect(lambda: os.system("adb kill-server"))
        self.get_device_info_Button.clicked.connect(self.get_device_info)

    def set_screen_size(self):
        self.screen_size = self.size_listWidget.currentItem().text()

    def set_screen_dpi(self):
        self.screen_dpi = self.dpi_listWidget.currentItem().text()

    def get_device_info(self):
        self.info_label.setText('目前裝置: {} \n裝置 sid : {} \n裝置環境: {}\n解析度: {}dpi: {}'.format(
            self.select_device_name,
            self.select_device_id,
            self.select_device_envi,
            self.get_device_size(),
            self.get_device_dpi(),
        ))

    def get_device_size(self):
        return os.popen('adb -s {}  shell wm size'.format(self.select_device_id)).read()

    def get_device_dpi(self):
        return os.popen('adb -s {}  shell wm density'.format(self.select_device_id)).read()

    def stop(self) -> None:
        self.close()


class Dialog3(QtWidgets.QDialog):

    def __init__(self, select_script: str = '', *args: Any, **kwargs: Any):
        super(Dialog3, self).__init__(*args, **kwargs)

        self.select_script = select_script

        self.setup_ui()
        self.show()

    def setup_ui(self):
        uic.loadUi(os.path.join(curPath, UI_ST.LOAD_SUB_UI[2]), self)  # type: ignore
        self.setWindowTitle(UI_ST.LOAD_SUB_UI[2])
        _image_path = curPath + f'\\script_info\\{self.select_script}.png'
        self._pyqt_img = cv2.imread(_image_path)

        height, width, _ = self._pyqt_img.shape

        bytesPerline = 3 * width
        self.qimg = QImage(self._pyqt_img, width, height, bytesPerline, QImage.Format.Format_RGB888).rgbSwapped()  #type: ignore
        self.qimg = self.qimg.scaled(1266, 585)
        self.img_label.setPixmap(QPixmap.fromImage(self.qimg))


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

#  pyinstaller -D -p #'curPath'