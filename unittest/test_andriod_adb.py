import unittest
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from autoscript_kernel.metis import MetisClass
from autoscript_kernel.params import ImageRecognitionParams


class TestMyModule(unittest.TestCase):

    def setUp(self):
        # Initialize your class object here
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]
        sys.path.append(rootPath)
        relatively_path = './{}/'.format(os.path.relpath(curPath, start=os.curdir))
        self.test_metis = MetisClass(
            device_id='test_device_id',
            sub_root_dict={
                'tmp_root': 'tmp/',
                'icon_root': 'icon/',
                'save_root': 'storage/temp/',
            },
            relatively_path=relatively_path,
            pyqt6_ui_label_dict='',
            os_environment='android',
        )
        self.test_metis.create_sub_root_file()
        self.test_metis.is_backup = False
        self.test_metis.screenshot_wait_time_increase = 1
        self.test_metis.is_check_gamelog = False

    @patch('os.system')
    @patch('autoscript_kernel.Metis_2_12.MetisClass')
    def test_tap_android(self, mock_wda_client, mock_os_system):
        # Set the _os_environment attribute to 'android'
        self.test_metis._os_environment = 'android'

        # Call the tap function
        self.test_metis.tap((100, 200))

        # Check if os.system was called with the correct adb command
        mock_os_system.assert_called_with("adb {} shell input tap {} {}".format(self.test_metis.get_device_id, 100, 200))

    @patch('os.system')
    @patch('autoscript_kernel.Metis_2_12.MetisClass')
    def test_swipe_android(self, mock_wda_client, mock_os_system):
        # Set the _os_environment attribute to 'android'
        self.test_metis._os_environment = 'android'
        # Call the tap function
        self.test_metis.swipe((100, 200), (100, 700), 300)

        # Check if os.system was called with the correct adb command
        mock_os_system.assert_called_with("adb  {} shell input swipe {} {} {} {} {}".format(
            self.test_metis.get_device_id, 100, 200, 100, 700, 300))

    @patch('os.system')
    def test_screenshot_android(self, mock_os_system):
        # Set the _os_environment attribute to 'android'
        self.test_metis._os_environment = 'android'

        # Call the screenshot function
        self.test_metis.screenshot()

        # Check if os.system was called with the correct adb commands
        mock_os_system.assert_any_call("adb  {}  shell screencap -p /sdcard/screenshot.png".format(
            self.test_metis.get_device_id))
        mock_os_system.assert_any_call("adb  {}  pull /sdcard/screenshot.png {}{}".format(
            self.test_metis.get_device_id, self.test_metis.get_current_root + self.test_metis.get_sub_root_path('tmp_root'),
            self.test_metis._check_image_name_pngFormat('tmp0.png')))


if __name__ == '__main__':
    unittest.main()