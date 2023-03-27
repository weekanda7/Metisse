import unittest
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from autoscript_kernel.Metis_2_12 import Metis_2_12_class



class TestMyModule(unittest.TestCase):

    def setUp(self):
        # Initialize your class object here
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]
        sys.path.append(rootPath)
        relatively_path = './{}/'.format(os.path.relpath(curPath, start=os.curdir))
        self.test_metis = Metis_2_12_class(
            device_id='test_device_id',
            sub_root_dict={
                'tmp_root': 'tmp/',
                'icon_root': 'icon/',
                'save_root': 'storage/temp/',
            },
            relatively_path=relatively_path,
            pyqt6_ui_label_dict='',
            os_environment='android',  # avoid calling wda_client
        )
        self.test_metis.create_sub_root_file()
        self.test_metis.is_backup = False
        self.test_metis.screenshot_wait_time_increase = 1
        self.test_metis.is_check_gamelog = False
    


    @patch('os.system')
    @patch('autoscript_kernel.Metis_2_12.Metis_2_12_class')
    def test_tap_ios(self, mock_wda_client, mock_os_system):
        # Set the _os_environment attribute to 'ios'
        self.test_metis._os_environment = 'ios'
        
        # Set up a MagicMock for wda_client
        self.test_metis.wda_client = MagicMock()

        # Call the tap function
        self.test_metis.tap((100, 200))

        # Check if wda_client.tap was called with the correct coordinates
        self.test_metis.wda_client.tap.assert_called_with(int(100 / self.test_metis.ios_device_scale),
                                                          int(200 / self.test_metis.ios_device_scale))


    @patch('os.system')
    @patch('autoscript_kernel.Metis_2_12.Metis_2_12_class')
    def test_swipe_ios(self, mock_wda_client, mock_os_system):
        # Set the _os_environment attribute to 'ios'
        self.test_metis._os_environment = 'ios'
        
        # Set up a MagicMock for wda_client
        self.test_metis.wda_client = MagicMock()

        # Call the tap function
        self.test_metis.swipe((100, 200),(100,700),300)

        # Check if wda_client.tap was called with the correct coordinates
        self.test_metis.wda_client.swipe.assert_called_with(int(100 / self.test_metis.ios_device_scale),
                                                          int(200 / self.test_metis.ios_device_scale),int(100 / self.test_metis.ios_device_scale),int(700 / self.test_metis.ios_device_scale),300/ 1000)


    def test_screenshot_ios(self):
        # Set the _os_environment attribute to 'ios'
        self.test_metis._os_environment = 'ios'

        # Set up a MagicMock for wda_client.screenshot()
        mock_screenshot = MagicMock()
        mock_screenshot.save = MagicMock()
        self.test_metis.wda_client = MagicMock()
        self.test_metis.wda_client.screenshot = MagicMock(return_value=mock_screenshot)

        # Call the screenshot function
        self.test_metis.screenshot()

        # Check if wda_client.screenshot().save() was called with the correct file path
        mock_screenshot.save.assert_called_with("{}{}".format(
            self.test_metis.get_current_root + self.test_metis.get_sub_root_path('tmp_root'),
            self.test_metis._check_image_name_pngFormat('tmp0.png')))




if __name__ == '__main__':
    unittest.main()