import os
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
