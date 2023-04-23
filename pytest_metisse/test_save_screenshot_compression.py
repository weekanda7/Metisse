import shutil
import tempfile
import os
import sys
import pytest
from PIL import Image


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.params import SaveParams, UiClientParams
from metisse.metisse import MetisseClass

curPath = os.path.abspath(os.path.dirname(__file__))



@pytest.fixture
def test_test_save_screenshot_compression_setup():
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

def test_save_screenshot_compression(test_test_save_screenshot_compression_setup):
    test_metisse = test_test_save_screenshot_compression_setup
    save_params = SaveParams(load_image_primary_dir='temp_image',
                                load_image_name='tmp0',
                                save_image_primary_dir='storage',
                                save_image_name='save0',
                                compression=0.5,
                                is_refresh_screenshot=False,
                                is_save_image_name_add_time=False)

    test_metisse.save_screenshot_compression(save_params)

    expected_output_path = os.path.join(test_metisse._script_path.device_id_path, save_params.save_image_primary_dir,
                                        save_params.save_image_name)
    print(expected_output_path)
    assert os.path.exists(expected_output_path) , 'Output file not found.'
    expected_output_path = os.path.join(test_metisse._script_path.device_id_path, save_params.save_image_primary_dir,
                                        save_params.save_image_name)
    assert os.path.exists(expected_output_path) , 'Output file not found.'

    with Image.open(expected_output_path) as output_image:  # avoid ResourceWarning
        with Image.open(
                os.path.join(test_metisse._script_path.device_id_path, save_params.load_image_primary_dir,
                                test_metisse._script_path._check_image_name_pngFormat(
                                    save_params.load_image_name))) as original_image:

            expected_size = tuple(int(x * save_params.compression) for x in original_image.size)
            assert output_image.size == expected_size, 'Output image size does not match expected size.'


if __name__ == '__main__':
    pytest.main(['-v','-s','pytest_metisse/test_save_screenshot_compression.py'])
