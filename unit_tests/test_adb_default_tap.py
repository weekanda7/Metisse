import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import other necessary modules and classes
from core.params import ImageRecognitionParams,UiClientParams
from core.metis import MetisClass


class TestMyModule(unittest.TestCase):

    # Omit setUp method
    def setUp(self):
        # Initialize your class object here
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]
        sys.path.append(rootPath)
        relatively_path = './{}/'.format(os.path.relpath(curPath, start=os.curdir))
        self.test_metis = MetisClass(
            device_id='test_virtual_device',
            relatively_path=relatively_path,
            pyqt6_ui_label_dict=UiClientParams(),
            os_environment='android',
        )
        self.test_metis.is_backup = True  # check save backup image
        self.test_metis.screenshot_wait_time_increase = 1
        self.test_metis.is_check_gamelog = False

    @patch.object(MetisClass, 'check_image_recognition', return_value=True)
    @patch.object(MetisClass, 'tap')
    @patch.object(MetisClass, 'save_screenshot_compression')
    def test_adb_default_tap(self, mock_save_screenshot_compression, mock_tap, mock_check_image_recognition):
        # Set up the necessary input parameters and objects
        params = ImageRecognitionParams(template_image_name="example_template",
                                        template_image_root_name="example_root_key",
                                        is_backup=True)

        # Call the adb_default_tap method with the prepared input parameters
        result = self.test_metis.adb_default_tap(params)

        # Check if the mocked methods were called with the expected arguments
        mock_check_image_recognition.assert_called_with(params)
        mock_tap.assert_called_once()
        mock_save_screenshot_compression.assert_called_once()

        # Assert the return value of the adb_default_tap method
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()