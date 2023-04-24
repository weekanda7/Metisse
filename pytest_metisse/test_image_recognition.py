import os
import sys
import pytest
import cv2
from cv2 import Mat
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import other necessary modules and classes
curPath = os.path.abspath(os.path.dirname(__file__))
from metisse.utils.image_recognition import match_template
from metisse.params import ImageRecognitionResult


@pytest.fixture()
def test_match_setup():
    # Load test images
    screen_image_path = os.path.join(curPath,'test_data','image', 'tmp0.png')
    template_image_path = os.path.join(
        curPath,'test_data','image', 'test_template.png')
    screen_image = cv2.imread(screen_image_path)
    template_image = cv2.imread(template_image_path)
    return screen_image, template_image

def test_match_template(test_match_setup):
    screen_image, template_image = test_match_setup
    # Set accuracy value
    accuracy_val = 0.9

    # Call the match_template function
    result = match_template(screen_image, template_image, accuracy_val)

    # Check if the result is an instance of ImageRecognitionResult
    assert isinstance(result, ImageRecognitionResult)

    # Check if the result attributes are correctly set
    expected_is_recognized = True
    expected_coordinate = (758, 951)
    expected_recognition_threshold = 0.9999983310699463
    assert result.is_recognized ==  expected_is_recognized
    assert result.coordinate ==  expected_coordinate
    assert result.recognition_threshold == pytest.approx(expected_recognition_threshold, abs=1e-2)


if __name__ == "__main__":
    pytest.main(['-v','-s','pytest_metisse/test_image_recognition.py'])