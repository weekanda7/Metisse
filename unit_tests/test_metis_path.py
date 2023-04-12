
import os
import sys
import unittest
from unittest import mock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metis.settings import Settings as ST
from metis.utils.metis_path import DevPath

class TestDevPath(unittest.TestCase):
    def setUp(self):
        # 使用mock替换print函数，以便捕获输出
        self.print_patcher = mock.patch("builtins.print")
        self.print_mock = self.print_patcher.start()

        # 测试相对路径
        self.relative_path = "unit_tests"

        # 计算绝对路径
        self.absolute_path = os.path.abspath(self.relative_path)

    def tearDown(self):
        # 清除测试文件夹
        _path = os.path.abspath(self.absolute_path)
        for _document_path in ST.DEV_ENVIRONMENT_ROOT_PATH:
            if os.path.exists(os.path.join(_path, _document_path)):
                os.removedirs(os.path.join(_path, _document_path))




    def test_init(self):
        dev_path = DevPath(self.absolute_path)
        self.assertEqual(dev_path._absolute_path, self.absolute_path)

        # 检查print输出
        #self.print_mock.assert_called_once_with("Path does not exist:", self.absolute_path)

    def test_initialize_dev_environment(self):
        dev_path = DevPath(self.absolute_path)
        dev_path.initialize_dev_environment()

        for _document_path in ST.DEV_ENVIRONMENT_ROOT_PATH:
            _document_path_temp = os.path.join(self.absolute_path, _document_path)
            self.assertTrue(os.path.isdir(_document_path_temp))

    def test_auto_generate_dev_path(self):
        DevPath.auto_generate_dev_path()

        # 获取调用auto_generate_dev_path方法的文件路径
        _path =os.path.abspath(self.absolute_path)

        for _document_path in ST.DEV_ENVIRONMENT_ROOT_PATH:
            _document_path_temp = os.path.join(_path, _document_path)
            self.assertTrue(os.path.isdir(_document_path_temp))

if __name__ == "__main__":
    unittest.main()