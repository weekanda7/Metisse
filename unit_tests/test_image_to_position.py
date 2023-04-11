
import os
import sys
import unittest
import cv2
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.params import ImageRecognitionParams,UiClientParams
from core.metis import MetisClass
curPath = os.path.abspath(os.path.dirname(__file__))

class TestMyModule(unittest.TestCase):

    def setUp(self):
        # Initialize your class object here
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]
        sys.path.append(rootPath)

        relatively_path = './{}/'.format(
            os.path.relpath(curPath, start=os.curdir))
        self.test_metis = MetisClass(
            device_id='test_virtual_device',
            relatively_path=relatively_path,
            pyqt6_ui_label_dict=UiClientParams(),
            os_environment='android',
        )
        self.test_metis.is_backup = False
        self.test_metis.screenshot_wait_time_increase = 1
        self.test_metis.is_check_gamelog = False

    def test_image_to_position(self):
        # Set up the necessary input parameters and objects
        # You need to replace the paths with the actual paths of your sample images

        screen_image_path = os.path.join(curPath,'test_virtual_device/tmp_root', 'tmp0.png')
        template_image_path = os.path.join(
            curPath,'test_virtual_device/icon', 'test_tamplate.png')

        screen_image = cv2.imread(screen_image_path, cv2.IMREAD_GRAYSCALE)
        template_image = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)

        accuracy_val = 0.8

        # Call the _image_to_position method with the prepared input parameters
        self.test_metis._image_to_position(
            screen_image, template_image, accuracy_val)

        # Check if the attributes have the expected values
        # You need to replace the expected values with the actual expected values
        expected_itp_bool = True
        expected_itp_center = (204, 197)
        expected_itp_max_val = 0.9999983310699463

        self.assertEqual(self.test_metis._itp_bool, expected_itp_bool)
        self.assertEqual(self.test_metis._itp_center, expected_itp_center)
        self.assertAlmostEqual(self.test_metis._itp_max_val,
                               expected_itp_max_val, places=2)

        # If needed, you can also check the _itp_center_list attribute
        # ...


if __name__ == '__main__':
    unittest.main()
