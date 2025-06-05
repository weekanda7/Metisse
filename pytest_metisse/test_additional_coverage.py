import os
import shutil
from unittest.mock import patch

import pytest
from PIL import Image

from metisse.metisse import MetisseClass
from metisse.params import (
    ImageRecognitionParams,
    ImageRecognitionResult,
    SaveParams,
    UiClientParams,
)


@pytest.fixture
def metisse_tmp(tmp_path):
    mc = MetisseClass(
        device_id="dev123",
        relatively_path=str(tmp_path),
        pyqt6_ui_label=UiClientParams(),
        os_environment="android",
    )
    mc._logger.close()
    src = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "test_data", "image", "tmp0.png"
    )
    dst = os.path.join(str(tmp_path), "dev123", "temp_image", "tmp0.png")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)
    yield mc
    shutil.rmtree(str(tmp_path))


def test_init_without_relatively_path(tmp_path):
    with patch.object(
        MetisseClass, "get_current_path", return_value=str(tmp_path)
    ) as m_get:
        mc = MetisseClass(
            device_id="device",
            relatively_path="",
            pyqt6_ui_label=UiClientParams(),
            os_environment="android",
        )
        mc._logger.close()
        assert mc._relatively_path == str(tmp_path)
        m_get.assert_called_once()


def test_get_device_id_empty(metisse_tmp):
    mc = metisse_tmp
    mc._device_id = ""
    assert mc.get_device_id == ""


def test_check_gamelog_missing_screen_image(tmp_path):
    cur = os.path.abspath(os.path.dirname(__file__))
    mc = MetisseClass(
        device_id="dev",
        relatively_path=str(tmp_path),
        pyqt6_ui_label=UiClientParams(),
        os_environment="android",
    )
    mc._logger.close()
    os.makedirs(os.path.join(str(tmp_path), "icon"), exist_ok=True)
    shutil.copy(
        os.path.join(cur, "test_data", "image", "test_template.png"),
        os.path.join(str(tmp_path), "icon", "log_button.png"),
    )
    params = ImageRecognitionParams()
    with patch.object(mc, "screenshot") as m_shot, patch(
        "metisse.metisse.image_recognition.match_template",
        return_value=ImageRecognitionResult(),
    ) as m_match:
        mc.check_gamelog(params)
        m_shot.assert_called_once()
        m_match.assert_called_once()


def test_save_screenshot_compression_refresh_add_time(metisse_tmp):
    mc = metisse_tmp
    sp = SaveParams(
        load_image_primary_dir="temp_image",
        load_image_name="tmp0",
        save_image_primary_dir="storage",
        save_image_name="save",
        compression=1,
        is_refresh_screenshot=True,
        screenshot_wait_time=0.1,
        is_save_image_name_add_time=True,
    )
    with patch("metisse.metisse.time.sleep") as m_sleep, patch.object(
        mc, "screenshot"
    ) as m_shot, patch("metisse.metisse.time.strftime", return_value="20250101_"):
        mc.save_screenshot_compression(sp)
        m_sleep.assert_called_once_with(sp.screenshot_wait_time)
        m_shot.assert_called_once()
    expected_name = "20250101_save.png"
    out_path = os.path.join(
        mc._script_path.device_id_path, sp.save_image_primary_dir, expected_name
    )
    assert os.path.exists(out_path)
    with Image.open(out_path) as img:
        assert (
            img.size
            == Image.open(
                os.path.join(mc._script_path.device_id_path, "temp_image", "tmp0.png")
            ).size
        )


def test_crop_screenshot_refresh_add_time(metisse_tmp):
    mc = metisse_tmp
    sp = SaveParams(
        save_image_primary_dir="storage",
        save_image_name="crop",
        is_refresh_screenshot=True,
        screenshot_wait_time=0.1,
        is_save_image_name_add_time=True,
    )
    with patch("metisse.metisse.time.sleep") as m_sleep, patch.object(
        mc, "screenshot"
    ) as m_shot, patch("metisse.metisse.time.strftime", return_value="20250101_"):
        mc.crop_screenshot((0, 0), (10, 10), sp)
        m_sleep.assert_called_once_with(sp.screenshot_wait_time)
        m_shot.assert_called_once()
    expected_name = "20250101_crop.png"
    out_path = os.path.join(
        mc._script_path.device_id_path, sp.save_image_primary_dir, expected_name
    )
    assert os.path.exists(out_path)
    with Image.open(out_path) as img:
        assert img.size == (10, 10)


def test_default_press_success_backup(metisse_tmp):
    mc = metisse_tmp
    mc.is_backup = True
    params = ImageRecognitionParams(template_image_name="tpl", is_backup=True)
    mc._img_recog_result.coordinate = (1, 1)
    with patch.object(
        mc, "check_image_recognition", return_value=True
    ) as m_check, patch.object(mc, "press") as m_press, patch.object(
        mc, "save_screenshot_compression"
    ) as m_save:
        result = mc.default_press(params)
        assert result is True
        m_check.assert_called_once_with(params)
        m_press.assert_called_once_with((1, 1), 300, 1, 0.0)
        m_save.assert_called_once()
