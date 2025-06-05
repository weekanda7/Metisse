import shutil
from unittest import mock

import pytest

from metisse.metisse import MetisseClass
from metisse.params import ImageRecognitionParams, UiClientParams


@pytest.fixture
def mc(tmp_path):
    mc = MetisseClass(
        device_id="dev",
        relatively_path=str(tmp_path),
        pyqt6_ui_label=UiClientParams(),
        os_environment="android",
    )
    mc._logger.close()
    mc.is_backup = True
    yield mc
    shutil.rmtree(str(tmp_path))


def test_perform_action_success(mc):
    params = ImageRecognitionParams(template_image_name="tpl", is_backup=True)
    action = mock.Mock()
    with mock.patch.object(
        mc, "check_image_recognition", return_value=True
    ) as m_check, mock.patch.object(
        mc, "save_screenshot_compression"
    ) as m_save, mock.patch.object(
        mc._logger, "info"
    ) as m_info, mock.patch.object(
        mc._ui_client, "send_log_to_ui"
    ) as m_send:
        result = mc._perform_action(params, action, "test")
        assert result is True
        m_check.assert_called_once_with(params)
        action.assert_called_once()
        m_info.assert_called()
        m_send.assert_called()
        m_save.assert_called_once()


def test_perform_action_failure(mc):
    params = ImageRecognitionParams(template_image_name="tpl", is_backup=True)
    action = mock.Mock()
    with mock.patch.object(
        mc, "check_image_recognition", return_value=False
    ) as m_check, mock.patch.object(
        mc, "save_screenshot_compression"
    ) as m_save, mock.patch.object(
        mc._logger, "info"
    ) as m_info, mock.patch.object(
        mc._ui_client, "send_log_to_ui"
    ) as m_send:
        result = mc._perform_action(params, action, "test")
        assert result is False
        m_check.assert_called_once_with(params)
        action.assert_not_called()
        m_info.assert_called()
        m_send.assert_called()
        m_save.assert_called_once()
