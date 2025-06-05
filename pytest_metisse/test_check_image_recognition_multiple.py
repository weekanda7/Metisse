import os
import shutil
from unittest.mock import patch

import pytest

from metisse.metisse import MetisseClass
from metisse.params import (
    ImageRecognitionParams,
    ImageRecognitionResult,
    UiClientParams,
)


@pytest.fixture
def metisse_multi_setup(tmp_path):
    cur_path = os.path.abspath(os.path.dirname(__file__))
    mc = MetisseClass(
        device_id="test_virtual_device",
        relatively_path=str(tmp_path),
        pyqt6_ui_label=UiClientParams(),
        os_environment="android",
    )
    mc._logger.close()
    mc.is_backup = False
    mc.screenshot_wait_time_increase = 0
    mc.is_check_gamelog = True

    shutil.copy(
        os.path.join(cur_path, "test_data", "image", "test_template.png"),
        os.path.join(str(tmp_path), "icon", "test_template.png"),
    )
    for name in ("tmp0.png", "tmp1.png"):
        shutil.copy(
            os.path.join(cur_path, "test_data", "image", "tmp0.png"),
            os.path.join(str(tmp_path), "test_virtual_device", "temp_image", name),
        )
    yield mc
    shutil.rmtree(str(tmp_path))


def test_check_image_recognition_multiple(metisse_multi_setup):
    mc = metisse_multi_setup
    params = ImageRecognitionParams(
        template_image_name="test_template",
        template_image_primary_dir="icon",
        compare_times_counter=2,
        repeatedly_screenshot_times=2,
        is_refresh_screenshot=False,
    )

    result_false = ImageRecognitionResult()
    result_false.is_recognized = False
    result_true = ImageRecognitionResult()
    result_true.is_recognized = True

    with patch.object(mc, "screenshot") as m_shot, patch.object(
        mc, "check_gamelog"
    ) as m_gamelog, patch("metisse.metisse.time.sleep"), patch(
        "metisse.metisse.image_recognition.match_template",
        side_effect=[result_false, result_false, result_true],
    ) as m_match:
        assert mc.check_image_recognition(params)
        assert m_gamelog.called
        assert m_shot.call_count >= 3
        assert m_match.call_count == 3
