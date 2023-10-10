import os
import shutil
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.example.generate_example import create_example_py_file


@pytest.fixture
def test_generate_example_setup():
    current_path = os.path.abspath(os.path.dirname(__file__))
    example_py_path = os.path.join(current_path, "script_example.py")
    icon_folder_path = os.path.join(current_path, "icon")
    temp_image_folder_path = os.path.join(
        current_path, "01234567(test_uid)", "temp_image"
    )
    ui_folder_path = os.path.join(current_path, "ui")
    device_folder_path = os.path.join(current_path, "01234567(test_uid)")
    yield example_py_path, icon_folder_path, temp_image_folder_path, ui_folder_path, device_folder_path
    if os.path.exists(example_py_path):
        os.remove(example_py_path)
    if os.path.exists(temp_image_folder_path):
        shutil.rmtree(temp_image_folder_path)
    if os.path.exists(icon_folder_path):
        shutil.rmtree(icon_folder_path)
    if os.path.exists(ui_folder_path):
        shutil.rmtree(ui_folder_path)
    if os.path.exists(device_folder_path):
        shutil.rmtree(device_folder_path)


def test_create_example_py_file(test_generate_example_setup):
    (
        example_py_path,
        icon_folder_path,
        temp_image_folder_path,
        ui_folder_path,
        device_folder_path,
    ) = test_generate_example_setup
    create_example_py_file()
    assert os.path.exists(example_py_path), "Example py file not created."
    assert os.path.exists(icon_folder_path), "Icon folder not created."
    assert os.path.exists(temp_image_folder_path), "Temp image folder not created."
    assert os.path.exists(ui_folder_path), "ui folder not created."


if __name__ == "__main__":
    pytest.main(["-v", "-s", "pytest_metisse/test_generate_example.py"])
