import os
import sys
import unittest
import cv2
import numpy as np
from PIL import Image

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from autoscript_kernel.metis import MetisClass
from autoscript_kernel.params import SaveParams


class TestCropScreenshot(unittest.TestCase):

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
            os_environment='android',  # avoid calling wda_client
        )
        self.test_metis.create_sub_root_file()
        self.test_metis.is_backup = False
        self.test_metis.screenshot_wait_time_increase = 1
        self.test_metis.is_check_gamelog = False

    def test_crop_screenshot(self):
        save_params = SaveParams(save_image_root_dict_key='save_root',
                                 save_image_name='test_cropped_image',
                                 save_image_additional_root='',
                                 is_refresh_screenshot=True,
                                 screenshot_wait_time=0.1,
                                 is_save_image_name_add_time=False,
                                 compression=1)

        coordinate1 = (100, 50)
        coordinate2 = (300, 400)

        self.test_metis.crop_screenshot(save_params, coordinate1, coordinate2)

        expected_output_path = os.path.join(self.test_metis.get_current_root,
                                            self.test_metis.get_sub_root_path(save_params.save_image_root_dict_key),
                                            self.test_metis._check_additional_root(save_params.save_image_additional_root),
                                            save_params.save_image_name + '.png')

        self.assertTrue(os.path.exists(expected_output_path), 'Cropped image file was not created.')

        with Image.open(expected_output_path) as cropped_image:
            expected_size = (coordinate2[0] - coordinate1[0], coordinate2[1] - coordinate1[1])
            self.assertEqual(cropped_image.size, expected_size, 'Cropped image size does not match expected size.')

    def tearDown(self):
        self.test_metis = None


if __name__ == '__main__':
    unittest.main()