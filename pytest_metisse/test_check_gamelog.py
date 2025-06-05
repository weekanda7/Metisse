import os
import shutil
from unittest import mock

import pytest

from metisse.metisse import MetisseClass
from metisse.params import ImageRecognitionParams, UiClientParams


@pytest.fixture
def gamelog_setup(tmp_path):
    cur_path = os.path.abspath(os.path.dirname(__file__))
    mc = MetisseClass(
        device_id="test_device",
        relatively_path=str(tmp_path),
        pyqt6_ui_label=UiClientParams(),
        os_environment="android",
    )
    mc._logger.close()
    mc.is_backup = False
    mc.screenshot_wait_time_increase = 1
    # copy required images
    shutil.copy(
        os.path.join(cur_path, "test_data", "image", "tmp0.png"),
        os.path.join(str(tmp_path), "test_device", "temp_image", "tmp0.png"),
    )
    shutil.copy(
        os.path.join(cur_path, "test_data", "image", "test_template.png"),
        os.path.join(str(tmp_path), "icon", "log_button.png"),
    )
    yield mc
    shutil.rmtree(str(tmp_path))


def test_check_gamelog_success(gamelog_setup):
    mc = gamelog_setup
    params = ImageRecognitionParams()
    with mock.patch.object(mc, "tap") as m_tap, mock.patch.object(
        mc._ui_client, "send_log_to_ui"
    ) as m_send, mock.patch.object(mc._ui_client, "send_image_path_to_ui") as m_img:
        mc.check_gamelog(params)
        assert mc._img_recog_result.is_recognized
        m_tap.assert_called_once()
        m_send.assert_called()
        m_img.assert_called()


def test_check_gamelog_missing_template(gamelog_setup):
    mc = gamelog_setup
    os.remove(os.path.join(str(mc._relatively_path), "icon", "log_button.png"))
    params = ImageRecognitionParams()
    with mock.patch.object(mc, "screenshot") as m_shot, mock.patch.object(
        mc._logger, "info"
    ) as m_info:
        mc.check_gamelog(params)
        m_shot.assert_not_called()
        m_info.assert_called()
        assert not mc._img_recog_result.is_recognized
