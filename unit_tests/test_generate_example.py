import sys
import unittest
import os
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metis.example.generate_example import create_example_py_file

class TestExample(unittest.TestCase):

    def setUp(self):
        self.current_path = os.path.abspath(os.path.dirname(__file__))
        self.example_py_path = os.path.join(self.current_path, "script_example.py")
        self.icon_folder_path = os.path.join(self.current_path, 'icon')
        self.temp_image_folder_path = os.path.join(self.current_path, '01234567(test_uid)', 'temp_image')
        self.ui_folder_path = os.path.join(self.current_path, 'ui')
    def tearDown(self):
        if os.path.exists(self.example_py_path):
            os.remove(self.example_py_path)
        if os.path.exists(self.temp_image_folder_path):
            shutil.rmtree(self.temp_image_folder_path)
        if os.path.exists(self.icon_folder_path):
            shutil.rmtree(self.icon_folder_path)
        if os.path.exists(self.ui_folder_path):
            shutil.rmtree(self.ui_folder_path)

    def test_create_example_py_file(self):
        create_example_py_file()
        self.assertTrue(os.path.exists(self.example_py_path), "Example py file not created.")
        self.assertTrue(os.path.exists(self.icon_folder_path), "Icon folder not created.")
        self.assertTrue(os.path.exists(self.temp_image_folder_path), "Temp image folder not created.")
        self.assertTrue(os.path.exists(self.ui_folder_path), "ui folder not created.")

if __name__ == "__main__":
    unittest.main()