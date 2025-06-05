import os
import shutil

import pytest

from metisse.params import SaveParams
from metisse.utils.metisse_path import ScriptPath


@pytest.fixture
def script_path_setup(tmp_path):
    sp = ScriptPath(str(tmp_path), "device")
    yield sp
    shutil.rmtree(str(tmp_path))


def test_check_image_name_pngFormat(script_path_setup):
    sp = script_path_setup
    assert sp._check_image_name_pngFormat("img") == "img.png"
    assert sp._check_image_name_pngFormat("icon.png") == "icon.png"


def test_check_path_creates_directory(script_path_setup, tmp_path):
    sp = script_path_setup
    new_dir = tmp_path / "new" / "nested"
    result = sp.check_path(str(new_dir))
    assert os.path.isdir(new_dir)
    assert result == str(new_dir)


def test_get_save_image_path(script_path_setup):
    sp = script_path_setup
    params = SaveParams(
        save_image_primary_dir="storage",
        save_image_secondary_dir="sec",
        save_image_name="img",
    )
    path = sp.get_save_image_path(params)
    expected = os.path.join(sp.device_id_path, "storage", "sec", "img.png")
    assert path == expected
