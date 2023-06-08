import inspect
import os
from ..metisse import MetisseClass
import shutil


def get_current_path() -> str:
    """
    get current path
    """
    caller_frame = inspect.stack()[2]
    caller_file_path = caller_frame.filename
    _path = os.path.dirname(os.path.abspath(caller_file_path))
    return _path


def copy_images(src_folder, dest_folder, extensions=('jpg', 'jpeg', 'png', 'gif')):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith(extensions):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, file)
                shutil.copy(src_path, dest_path)


def copy_ui(src_folder, dest_folder, extensions='gui'):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            if extensions in file.lower():
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, file)
                shutil.copy(src_path, dest_path)


def example():
    print(get_current_path())


def create_example_py_file():
    _path = get_current_path()
    _tmp = MetisseClass('01234567(test_uid)', _path, None, 'android')
    _tmp._logger.close()
    _curPath = os.path.abspath(os.path.dirname(__file__))

    source_folder = os.path.join(_curPath, "example_data", 'icon')
    destination_folder = os.path.join(_path, 'icon', 'script_example')
    copy_images(source_folder, destination_folder)

    source_folder = os.path.join(_curPath, "example_data", 'temp_image')
    destination_folder = os.path.join(_path, '01234567(test_uid)', 'temp_image')
    copy_images(source_folder, destination_folder)

    source_folder = os.path.join(_curPath, "example_data", 'ui')
    destination_folder = os.path.join(_path, 'ui')
    copy_ui(source_folder, destination_folder)

    content = '''import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.metisse import MetisseClass
from metisse.params import ImageRecognitionParams , SaveParams
TEMPLATE = {'template_image_secondary_dir' : 'script_example'}
SAVE = {'save_image_secondary_dir' : 'script_example'}

class script_example(MetisseClass):

    def __init__(self, device_id='', relatively_path='', pyqt6_ui_label={}, os_environment=''):
        MetisseClass.__init__(
            self,
            device_id=device_id,
            relatively_path=relatively_path,
            pyqt6_ui_label=pyqt6_ui_label,
            os_environment=os_environment,
        )

    def __call__(self, *args, **kwargs):
        self.check_image_recognition(
            ImageRecognitionParams(screen_image_name='tmp0',
                                   template_image_name='example_template_hand',
                                   is_refresh_screenshot=False,**TEMPLATE))  # simulate image recognition hand icon
        print(f'hand pos = {self._img_recog_result.coordinate}')

        self.execute_time_sleep(1)  # wait 1 second

        self.default_tap(
            ImageRecognitionParams(screen_image_name='tmp0',
                                   template_image_name='example_template_face',
                                   template_image_secondary_dir='script_example',
                                   is_refresh_screenshot=False))  # simulate image recognition face icon and tap face pos
        self.default_tap(
            ImageRecognitionParams(screen_image_name='tmp0',
                                   template_image_name='example_template_face',
                                   is_refresh_screenshot=False,**TEMPLATE))  # simulate image recognition face icon and tap face pos

        self.save_screenshot_compression( SaveParams(
                       save_image_name='save_image',
                       save_image_primary_dir='storage',
                       save_image_secondary_dir='script_example',
                       compression=0.5,
                       screenshot_wait_time=1,
                       is_save_image_name_add_time=True,
                       is_refresh_screenshot=False,
                       ))
        self.save_screenshot_compression( SaveParams(
                       save_image_name='save_image',
                       save_image_primary_dir='storage',
                       compression=0.5,
                       screenshot_wait_time=1,
                       is_save_image_name_add_time=True,
                       is_refresh_screenshot=False,
                       **SAVE,
                       ))
        self.save_screenshot_compression( SaveParams(
                       save_image_name='save_image',
                       save_image_primary_dir='storage',
                       save_image_subdirs = ['third','forth'],
                       compression=0.5,
                       screenshot_wait_time=1,
                       is_save_image_name_add_time=True,
                       is_refresh_screenshot=False,
                       **SAVE,
                       ))
        self.crop_screenshot((288, 260), (340, 294),
                             SaveParams(load_image_primary_dir='temp_image',
                                        save_image_primary_dir='storage',
                                        save_image_name='eyes',
                                        load_image_name='tmp0',
                                        is_refresh_screenshot=False))
        self.crop_screenshot((288, 260), (340, 294),
                             SaveParams(load_image_primary_dir='temp_image',
                                        save_image_primary_dir='temp_image',
                                        save_image_secondary_dir='crop',
                                        save_image_name='small_image_tmp',
                                        load_image_name='tmp0',
                                        is_refresh_screenshot=False))
        self.default_tap(
            ImageRecognitionParams(screen_image_name='tmp0',
                                   template_image_name='small_image_tmp',
                                   template_image_primary_dir='temp_image',
                                   template_image_secondary_dir='crop',
                                   is_refresh_screenshot=False))  # simulate image recognition face icon and tap face pos


if __name__ == '__main__':
    script_obj = script_example('01234567(test_uid)', None, None, 'android')
    script_obj()
'''

    with open(os.path.join(_path, "script_example.py"), "w", encoding="utf-8") as file:
        file.write(content)
