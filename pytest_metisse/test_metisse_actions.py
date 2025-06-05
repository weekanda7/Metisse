import shutil
from unittest import mock

import pytest

from metisse.metisse import MetisseClass
from metisse.params import ImageRecognitionParams, UiClientParams


@pytest.fixture
def metisse_actions_setup(tmp_path):
    mc = MetisseClass(
        device_id="test_device",
        relatively_path=str(tmp_path),
        pyqt6_ui_label=UiClientParams(),
        os_environment="android",
    )
    mc._logger.close()
    mc.is_backup = False
    yield mc
    shutil.rmtree(str(tmp_path))


def test_screenshot_calls_client(metisse_actions_setup):
    mc = metisse_actions_setup
    expected_path = mc._script_path.get_image_path("snap.png", "temp_image", "")
    with mock.patch.object(mc._client, "screenshot") as m_screenshot, mock.patch.object(
        mc._logger, "debug"
    ) as m_debug, mock.patch.object(mc._ui_client, "send_log_to_ui") as m_send:
        mc.screenshot("snap.png", "temp_image", "")
        m_screenshot.assert_called_once_with(expected_path)
        m_debug.assert_called_once()
        m_send.assert_called_once()


def test_default_swipe_success(metisse_actions_setup):
    mc = metisse_actions_setup
    mc.is_backup = True
    params = ImageRecognitionParams(template_image_name="tpl")
    mc._img_recog_result.coordinate = (10, 20)
    with mock.patch.object(
        mc, "check_image_recognition", return_value=True
    ) as m_check, mock.patch.object(mc, "swipe") as m_swipe, mock.patch.object(
        mc, "save_screenshot_compression"
    ) as m_save:
        params.is_backup = True
        result = mc.default_swipe(params, (5, 5), 123, 2, 0.0)
        assert result is True
        m_check.assert_called_once_with(params)
        m_swipe.assert_called_once_with((10, 20), (5, 5), 123, 2, 0.0)
        m_save.assert_called_once()


def test_default_swipe_fail_backup(metisse_actions_setup):
    mc = metisse_actions_setup
    mc.is_backup = True
    params = ImageRecognitionParams(template_image_name="tpl", is_backup=True)
    with mock.patch.object(
        mc, "check_image_recognition", return_value=False
    ) as m_check, mock.patch.object(mc, "swipe") as m_swipe, mock.patch.object(
        mc, "save_screenshot_compression"
    ) as m_save:
        result = mc.default_swipe(params)
        assert result is False
        m_check.assert_called_once_with(params)
        m_swipe.assert_not_called()
        m_save.assert_called_once()


def test_default_press_success(metisse_actions_setup):
    mc = metisse_actions_setup
    params = ImageRecognitionParams(template_image_name="tpl")
    mc._img_recog_result.coordinate = (5, 5)
    with mock.patch.object(
        mc, "check_image_recognition", return_value=True
    ) as m_check, mock.patch.object(mc, "press") as m_press:
        result = mc.default_press(params, 300, 1, 0.0)
        assert result is True
        m_check.assert_called_once_with(params)
        m_press.assert_called_once_with((5, 5), 300, 1, 0.0)


def test_press_handles_oserror(metisse_actions_setup):
    mc = metisse_actions_setup
    with mock.patch.object(
        mc, "swipe", side_effect=OSError("fail")
    ) as m_swipe, mock.patch.object(
        mc._logger, "exception"
    ) as m_exc, mock.patch.object(
        mc._ui_client, "send_log_to_ui"
    ) as m_send:
        mc.press(
            (1, 2),
            pressing_time=100,
            press_execute_counter_times=1,
            press_execute_wait_time=0,
        )
        m_swipe.assert_called_once()
        m_exc.assert_called_once()
        m_send.assert_called_once()


def test_press_success_calls_swipe_and_logs(metisse_actions_setup):
    mc = metisse_actions_setup
    with mock.patch.object(mc, "swipe") as m_swipe, mock.patch.object(
        mc._logger, "info"
    ) as m_info, mock.patch.object(
        mc._ui_client, "send_log_to_ui"
    ) as m_send, mock.patch(
        "metisse.metisse.time.sleep"
    ) as m_sleep:
        mc.press(
            (3, 4),
            pressing_time=50,
            press_execute_counter_times=2,
            press_execute_wait_time=0,
        )
        assert m_swipe.call_count == 2
        m_info.assert_called_with(
            "adb_press method : (x,y) = %s pressing_time = %d", (3, 4), 50
        )
        m_send.assert_called_with(
            "adb_press method : \n (x,y) = (3, 4) \n pressing_time = 50"
        )
        m_sleep.assert_called()
