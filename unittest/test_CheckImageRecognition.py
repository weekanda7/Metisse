
import sys
import unittest
import tempfile
import os
import shutil

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from autoscript_kernel.params import ImageRecognitionParams
from autoscript_kernel.metis import MetisClass

class TestCheckImageRecognition(unittest.TestCase):

    def setUp(self):
        # Set up a temporary directory for storing test images
        self.test_dir = tempfile.mkdtemp()

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

        # Copy test images to the temporary directory
        src_test_images = curPath + '/tmp'
        dst_test_images = os.path.join(self.test_dir, 'tmp.png')
        shutil.copytree(src_test_images, dst_test_images)

    def tearDown(self):
        # Clean up the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_check_image_recognition_basic(self):
        # Create a basic ImageRecognitionParams object
        params = ImageRecognitionParams(
            template_image_name='test_tamplate',
            template_image_root_dict_key='icon_root',
            # Fill in other appropriate values for the parameters
        )

        result = self.test_metis.check_image_recognition(params)
        self.assertTrue(
            result, "check_image_recognition failed with basic params")

    def test_check_image_recognition_specific_case(self):
        # Create a specific ImageRecognitionParams object for a particular test case
        params = ImageRecognitionParams(
            template_image_name='test_tamplate',
            template_image_root_dict_key='icon_root',
            # Fill in other appropriate values for the parameters
        )

        result = self.test_metis.check_image_recognition(params)
        self.assertTrue(
            result, "check_image_recognition failed with specific params")

    # Add more test methods as needed to cover various aspects of the check_image_recognition method


if __name__ == '__main__':
    unittest.main()
