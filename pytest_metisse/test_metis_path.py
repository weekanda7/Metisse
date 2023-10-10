import os
import sys
from unittest import mock

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.settings import Settings as ST
from metisse.utils.metisse_path import DevPath


@pytest.fixture
def test_dev_path_setup():
    with mock.patch("builtins.print") as print_mock:
        relative_path = "pytest_metisse"
        absolute_path = os.path.abspath(relative_path)

        yield absolute_path, print_mock

        for _document_path in ST.DEV_ENVIRONMENT_ROOT_PATH:
            if os.path.exists(os.path.join(absolute_path, _document_path)):
                os.removedirs(os.path.join(absolute_path, _document_path))


def test_init(test_dev_path_setup):
    absolute_path, print_mock = test_dev_path_setup
    dev_path = DevPath(absolute_path)
    assert dev_path._absolute_path == absolute_path


def test_initialize_dev_environment(test_dev_path_setup):
    absolute_path, _ = test_dev_path_setup
    dev_path = DevPath(absolute_path)
    dev_path.initialize_dev_environment()

    for _document_path in ST.DEV_ENVIRONMENT_ROOT_PATH:
        _document_path_temp = os.path.join(absolute_path, _document_path)
        assert os.path.isdir(_document_path_temp)


def test_auto_generate_dev_path(test_dev_path_setup):
    absolute_path, _ = test_dev_path_setup
    DevPath.auto_generate_dev_path()

    for _document_path in ST.DEV_ENVIRONMENT_ROOT_PATH:
        _document_path_temp = os.path.join(absolute_path, _document_path)
        print(
            f"Checking directory: {_document_path_temp}"
        )  # Add this line to print debug info
        assert os.path.isdir(_document_path_temp)


if __name__ == "__main__":
    pytest.main(["-v", "-s", "pytest_metisse/test_metis_path.py"])
