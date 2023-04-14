import cv2
from cv2 import Mat
from ..params import ImageRecognitionResult
import numpy as np  # type: ignore


def match_template(_screen_image_mat: Mat, _template_image_mat: Mat, _accuracy_val: float) -> ImageRecognitionResult:
    _img_recog_result = ImageRecognitionResult()
    image_x, image_y = _template_image_mat.shape[:2]
    result = cv2.matchTemplate(_screen_image_mat, _template_image_mat, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)  # type: ignore unused var

    if max_val > _accuracy_val:  # accuracy between two image
        _temp_center = (int(max_loc[0] + image_y / 2), int(max_loc[1] + image_x / 2))
        _img_recog_result.is_recognized = True
        _img_recog_result.coordinate = _temp_center
        _img_recog_result.recognition_threshold = max_val
        loc = np.where(result >= _accuracy_val)  # type: ignore
        loc_ren = len(loc[-1][:])  # type: ignore
        if loc_ren > 0:
            _temp_center_list = []
            for i in range(loc_ren):
                _temp_center = (int(loc[1][i] + image_y / 2), int(loc[0][i] + image_x / 2))  # type: ignore
                _temp_center_list.append(_temp_center)  # type: ignore
                #if (): print("pos:", _temp_center)
            _img_recog_result.coordinates_list = _temp_center_list
    else:
        _img_recog_result.is_recognized = False
        _img_recog_result.coordinate = (0, 0)
        _img_recog_result.recognition_threshold = max_val
    return _img_recog_result
