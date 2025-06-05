import os
import shutil

from metisse.settings import Settings as ST
from metisse.utils.metisse_path import ScriptPath


def test_auto_generate_script_path():
    device_id = "pytest_device_auto"
    script_path = ScriptPath.auto_generate_script_path(device_id)
    expected_device_dir = os.path.join(os.path.dirname(__file__), device_id)
    try:
        assert script_path.device_id_path == os.path.abspath(expected_device_dir)
        for sub in ST.SCRIPT_ENVIRONMENT_ROOT_PATH:
            assert os.path.isdir(os.path.join(expected_device_dir, sub))
    finally:
        if os.path.exists(expected_device_dir):
            shutil.rmtree(expected_device_dir)
