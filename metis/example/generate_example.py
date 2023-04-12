import inspect
import os
from ..metis import  MetisClass
import shutil


def get_current_path()-> str:
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

def example():
    print(get_current_path())

def create_example_py_file():
    _path=get_current_path()
    MetisClass('test', _path, None , 'android')
    _curPath = os.path.abspath(os.path.dirname(__file__))
    source_folder =os.path.join(_curPath, "example_data",'icon')
    destination_folder = os.path.join(_path,'icon')
    copy_images(source_folder, destination_folder)
    source_folder =os.path.join(_curPath, "example_data",'temp_image')
    destination_folder = os.path.join(_path,'test','temp_image')
    copy_images(source_folder, destination_folder)
    content = '''import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metis.metis import MetisClass
from metis.params import ImageRecognitionParams

class Example(MetisClass):

    def __init__(self, device_id='',relatively_path='', pyqt6_ui_label_dict={}, os_environment=''):
        MetisClass.__init__(
            self,
            device_id=device_id,
            relatively_path= relatively_path,
            pyqt6_ui_label_dict=pyqt6_ui_label_dict,
            os_environment=os_environment,
        )
    def example(self):
        self.check_image_recognition(ImageRecognitionParams(screen_image_name='example_screen',template_image_name='example_template_hand',is_refresh_screenshot=False)) # simulate image recognition hand icon
        print(f'hand pos = {self._img_recog_result.coordinate}')

        self.execute_time_sleep(1) # wait 1 second


        self.adb_default_tap(ImageRecognitionParams(screen_image_name='example_screen',template_image_name='example_template_face',is_refresh_screenshot=False)) # simulate image recognition face icon and tap face pos


a = Example('test', None, None , 'android')
a.example()
'''

    with open(os.path.join(_path,"test1.py"), "w", encoding="utf-8") as file:
        file.write(content)

