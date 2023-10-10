import os
import shutil
import sys
import tempfile
from unittest.mock import patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.metisse import MetisseClass
from metisse.params import ImageRecognitionParams, UiClientParams


@pytest.fixture(scope="module")
def metisse_test_setup():
    test_dir = tempfile.mkdtemp()
    curPath = os.path.abspath(os.path.dirname(__file__))
    test_metisse = MetisseClass(
        device_id="test_virtual_device",
        relatively_path=test_dir,
        pyqt6_ui_label=UiClientParams(),
        os_environment="android",
    )
    test_metisse._logger.close()
    test_metisse.is_backup = False
    test_metisse.screenshot_wait_time_increase = 1
    test_metisse.is_check_gamelog = False

    src_test_images = os.path.join(curPath, "test_data", "image", "test_template.png")
    dst_test_images = os.path.join(test_dir, "icon", "test_template.png")
    shutil.copy(src_test_images, dst_test_images)

    src_test_images = os.path.join(
        curPath, "test_data", "image", "test_template_fail.png"
    )
    dst_test_images = os.path.join(test_dir, "icon", "test_template_fail.png")
    shutil.copy(src_test_images, dst_test_images)

    src_test_images = os.path.join(curPath, "test_data", "image", "tmp0.png")
    dst_test_images = os.path.join(
        test_dir, "test_virtual_device", "temp_image", "tmp0.png"
    )
    shutil.copy(src_test_images, dst_test_images)

    yield test_metisse
    shutil.rmtree(test_dir)


def test_check_image_recognition_basic(metisse_test_setup):
    params = ImageRecognitionParams(
        template_image_name="test_template",
        template_image_primary_dir="icon",
    )
    with patch(
        "metisse.metisse.MetisseClass.screenshot", return_value=None
    ) as mock_screenshot:
        result = metisse_test_setup.check_image_recognition(params)
        mock_screenshot.assert_called_once()
    assert result, "check_image_recognition failed with basic params"


def test_check_image_recognition_specific_case(metisse_test_setup):
    params = ImageRecognitionParams(
        template_image_name="test_template_fail",
        template_image_primary_dir="icon",
    )

    with patch(
        "metisse.metisse.MetisseClass.screenshot", return_value=None
    ) as mock_screenshot:
        result = metisse_test_setup.check_image_recognition(params)
        mock_screenshot.assert_called_once()
    assert not result, "check_image_recognition failed with specific params"


if __name__ == "__main__":
    pytest.main(["-v", "-s", "pytest_metisse/test_check_image_recognition.py"])
