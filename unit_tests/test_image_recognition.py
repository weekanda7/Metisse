import os
import sys
import unittest
import cv2
from cv2 import Mat
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import other necessary modules and classes
curPath = os.path.abspath(os.path.dirname(__file__))
from core.utils.image_recognition import match_template
from core.params import ImageRecognitionResult

class TestImageRecognition(unittest.TestCase):

    def test_match_template(self):
        # Load test images
        screen_image_path = os.path.join(curPath,'test_virtual_device/temp_image', 'tmp0.png')
        template_image_path = os.path.join(
            curPath,'test_virtual_device/icon', 'test_tamplate.png')

        screen_image = cv2.imread(screen_image_path)
        template_image = cv2.imread(template_image_path)



        # Set accuracy value
        accuracy_val = 0.9

        # Call the match_template function
        result = match_template(screen_image, template_image, accuracy_val)

        # Check if the result is an instance of ImageRecognitionResult
        self.assertIsInstance(result, ImageRecognitionResult)

        # Check if the result attributes are correctly set
        expected_is_recognized = True
        expected_coordinate = (204, 197)
        expected_recognition_threshold = 0.9999983310699463
        self.assertEqual(result.is_recognized, expected_is_recognized)
        self.assertEqual(result.coordinate, expected_coordinate)
        self.assertAlmostEqual(result.recognition_threshold,
                               expected_recognition_threshold, places=2)





if __name__ == "__main__":
    unittest.main()