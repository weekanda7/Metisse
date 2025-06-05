import os
from pathlib import Path

from metisse.example import generate_example


def _wrapper_path() -> str:
    return generate_example.get_current_path()


def test_get_current_path_func():
    expected = os.path.dirname(os.path.abspath(__file__))
    assert _wrapper_path() == expected


def test_copy_images_and_ui(tmp_path):
    src_img = tmp_path / "src_img"
    src_ui = tmp_path / "src_ui"
    dest_img = tmp_path / "dest_img"
    dest_ui = tmp_path / "dest_ui"
    src_img.mkdir()
    src_ui.mkdir()
    (src_img / "a.png").write_text("data")
    (src_img / "b.txt").write_text("other")
    (src_ui / "main.gui").write_text("ui")
    generate_example.copy_images(str(src_img), str(dest_img))
    generate_example.copy_ui(str(src_ui), str(dest_ui))
    assert (dest_img / "a.png").exists()
    assert not (dest_img / "b.txt").exists()
    assert (dest_ui / "main.gui").exists()
