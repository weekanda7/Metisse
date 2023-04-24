import os
import shutil
import sys
import tempfile
import pytest
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.params import SaveParams, UiClientParams
from metisse.metisse import MetisseClass




@pytest.fixture
def test_crop_screenshot_setup():
    test_dir = tempfile.mkdtemp()
    curPath = os.path.abspath(os.path.dirname(__file__))
    test_metisse = MetisseClass(
        device_id='test_virtual_device',
        relatively_path=test_dir,
        pyqt6_ui_label=UiClientParams(),
        os_environment='android',
    )
    test_metisse._logger.close()
    test_metisse.is_backup = False
    test_metisse.screenshot_wait_time_increase = 1
    test_metisse.is_check_gamelog = False

    src_test_images = os.path.join(curPath,'test_data','image','tmp0.png')
    dst_test_images = os.path.join(test_dir,'test_virtual_device','temp_image' ,'tmp0.png')
    shutil.copy(src_test_images, dst_test_images)

    yield test_metisse
    shutil.rmtree(test_dir)

def test_crop_screenshot(test_crop_screenshot_setup):
    test_metisse = test_crop_screenshot_setup
    save_params = SaveParams(save_image_primary_dir='storage',
                                save_image_name='test_cropped_image',
                                save_image_secondary_dir='',
                                is_refresh_screenshot=False,
                                screenshot_wait_time=0.1,
                                is_save_image_name_add_time=False,
                                compression=1)

    coordinate1 = (100, 50)
    coordinate2 = (300, 400)

    test_metisse.crop_screenshot(coordinate1, coordinate2, save_params)

    expected_output_path = os.path.join(test_metisse._script_path.device_id_path, save_params.save_image_primary_dir,
                                        save_params.save_image_name)
    assert os.path.exists(expected_output_path) , 'Cropped image file was not created.'

    with Image.open(expected_output_path) as cropped_image:
        expected_size = (coordinate2[0] - coordinate1[0], coordinate2[1] - coordinate1[1])
        assert cropped_image.size == expected_size, 'Cropped image size does not match expected size.'




if __name__ == '__main__':
    pytest.main(['-v','-s','pytest_metisse/test_crop_screenshot.py'])
