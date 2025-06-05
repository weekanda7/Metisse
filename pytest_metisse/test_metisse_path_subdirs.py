import os
import shutil

from metisse.params import ImageRecognitionParams, SaveParams
from metisse.utils.metisse_path import ScriptPath


def test_path_functions_with_subdirs(tmp_path):
    sp = ScriptPath(str(tmp_path), "device")

    img_params = ImageRecognitionParams(
        screen_image_name="shot",
        screen_image_primary_dir="temp_image",
        screen_image_secondary_dir="sec",
        screen_image_subdirs=["a", "b"],
    )
    screen_path = sp.get_screen_image_path(img_params)
    expected_screen = os.path.join(
        sp.device_id_path,
        "temp_image",
        "sec",
        "a",
        "b",
        "shot.png",
    )
    assert screen_path == expected_screen

    tmpl_params = ImageRecognitionParams(
        template_image_name="tpl",
        template_image_primary_dir="temp_image",
        template_image_secondary_dir="sec",
        template_image_subdirs=["c"],
    )
    template_path = sp.get_template_image_path(tmpl_params)
    expected_template = os.path.join(
        sp.device_id_path,
        "temp_image",
        "sec",
        "c",
        "tpl.png",
    )
    assert template_path == expected_template

    tmpl_params2 = ImageRecognitionParams(
        template_image_name="tpl2",
        template_image_primary_dir="icon",
        template_image_secondary_dir="sec2",
        template_image_subdirs=["d"],
    )
    template_path2 = sp.get_template_image_path(tmpl_params2)
    expected_template2 = os.path.join(
        sp.absolute_path,
        "icon",
        "sec2",
        "d",
        "tpl2.png",
    )
    assert template_path2 == expected_template2

    save_params = SaveParams(
        load_image_name="shot",
        load_image_secondary_dir="old",
        load_image_subdirs=["l1"],
        save_image_name="out",
        save_image_secondary_dir="new",
        save_image_subdirs=["s1"],
    )
    load_path = sp.get_load_image_path(save_params)
    expected_load = os.path.join(
        sp.device_id_path,
        "temp_image",
        "old",
        "l1",
        "shot.png",
    )
    assert load_path == expected_load

    save_path = sp.get_save_image_path(save_params)
    expected_save = os.path.join(
        sp.device_id_path,
        "storage",
        "new",
        "s1",
        "out.png",
    )
    assert save_path == expected_save

    shutil.rmtree(str(tmp_path))
