
import unittest
import os
import sys
import unittest
import cv2
from PIL import Image
import numpy as np

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from autoscript_kernel.params import SaveParams
from autoscript_kernel.metis import MetisClass


class TestSaveScreenshotCompression(unittest.TestCase):

    def setUp(self):
        # Initialize your class object here
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]
        sys.path.append(rootPath)
        relatively_path = './{}/'.format(
            os.path.relpath(curPath, start=os.curdir))
        self.test_metis = MetisClass(
            device_id='test_device_id',
            sub_root_dict={
                'tmp_root': 'tmp/',
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


    def test_save_screenshot_compression(self):
        save_params = SaveParams(load_image_root_dict_key='tmp_root',
                                 load_image_name='tmp0',
                                 save_image_root_dict_key='save_root',
                                 save_image_name='save0',
                                 compression=0.5,
                                 is_refresh_screenshot=False,
                                 is_save_image_name_add_time=False)

        self.test_metis.save_screenshot_compression(save_params)

        expected_output_path = os.path.join(self.test_metis.get_current_root, self.test_metis.get_sub_root_path(
            save_params.save_image_root_dict_key), save_params.save_image_name + '.png')
        self.assertTrue(os.path.exists(expected_output_path),
                        'Output file not found.')

        with Image.open(expected_output_path) as output_image:  # avoid ResourceWarning
            with Image.open(
                    os.path.join(self.test_metis.get_current_root,
                                 self.test_metis.get_sub_root_path(save_params.load_image_root_dict_key),
                                 self.test_metis._check_image_name_pngFormat(save_params.load_image_name))) as original_image:

                expected_size = tuple(int(x * save_params.compression)
                                      for x in original_image.size)
                self.assertEqual(output_image.size, expected_size,
                                 'Output image size does not match expected size.')



if __name__ == '__main__':
    unittest.main()
