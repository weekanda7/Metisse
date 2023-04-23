import shutil
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import other necessary modules and classes
from metisse.params import ImageRecognitionParams, UiClientParams
from metisse.metisse import MetisseClass


@pytest.fixture
def test_default_tap_setUp():
    test_dir = tempfile.mkdtemp()
    curPath = os.path.abspath(os.path.dirname(__file__))
    test_metisse = MetisseClass(
        device_id='test_virtual_device',
        relatively_path=test_dir,
        pyqt6_ui_label=UiClientParams(),
        os_environment='android',
    )
    test_metisse._logger.close()
    test_metisse.is_backup = True
    test_metisse.screenshot_wait_time_increase = 1
    test_metisse.is_check_gamelog = False

    src_test_images = os.path.join(curPath, 'test_data','image','test_template.png')
    dst_test_images = os.path.join(test_dir,'icon' ,'test_template.png')
    shutil.copy(src_test_images, dst_test_images)

    src_test_images = os.path.join(curPath, 'test_data','image','test_template_fail.png')
    dst_test_images = os.path.join(test_dir,'icon' ,'test_template_fail.png')
    shutil.copy(src_test_images, dst_test_images)

    src_test_images = os.path.join(curPath,'test_data','image','tmp0.png')
    dst_test_images = os.path.join(test_dir,'test_virtual_device','temp_image' ,'tmp0.png')
    shutil.copy(src_test_images, dst_test_images)

    yield test_metisse
    shutil.rmtree(test_dir)

@patch.object(MetisseClass, 'check_image_recognition', return_value=True)
@patch.object(MetisseClass, 'tap')
@patch.object(MetisseClass, 'save_screenshot_compression')
def test_adb_default_tap(mock_save_screenshot_compression, mock_tap, mock_check_image_recognition,test_default_tap_setUp):
    # Set up the necessary input parameters and objects
    params = ImageRecognitionParams(template_image_name="test_template",
                                    template_image_primary_dir="icon",
                                    is_backup=True)

    # Call the default_tap method with the prepared input parameters
    result = test_default_tap_setUp.default_tap(params)

    # Check if the mocked methods were called with the expected arguments
    mock_check_image_recognition.assert_called_with(params)
    mock_tap.assert_called_once()
    mock_save_screenshot_compression.assert_called_once()

    # Assert the return value of the default_tap method
    assert result, "check_image_recognition failed with basic params"



if __name__ == '__main__':
    pytest.main(['-v','-s','pytest_metisse/test_default_tap.py'])
