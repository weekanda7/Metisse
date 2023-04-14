# metis Package Documentation

metis is a Python library for automating image recognition and manipulation tasks. It provides a set of user-friendly methods that allow users to perform automated tapping, swiping, and pressing operations using image recognition techniques. Below is a brief overview of the main features and usage of metis:

## MetisClass

MetisClass is the primary class in metis containing all the basic image recognition and manipulation methods. To use metis, you need to create a subclass inheriting from MetisClass and implement custom methods as needed.

### Methods:

- `check_image_recognition()`: Checks the image recognition results.
- `default_tap()`: Performs a tap operation on the recognized image.
- `default_swipe()`: Performs a swipe operation on the recognized image.
- `default_press()`: Performs a press operation on the recognized image.
- `save_screenshot_compression()`: Saves a compressed screenshot.
- `crop_screenshot()`: Crops and saves a screenshot.
- `execute_time_sleep()`: Waits for a specified amount of time.

## ImageRecognitionParams

ImageRecognitionParams is a class for configuring image recognition parameters. Users can customize this class as needed for use in metis methods.

### Parameters:

- `screen_image_name`: The name of the screen image.
- `template_image_name`: The name of the template image.
- `template_image_primary_dir`: The primary directory of the template image.
- `template_image_secondary_dir`: The secondary directory of the template image.
- `is_refresh_screenshot`: Whether to refresh the screenshot.

## SaveParams

SaveParams is a class for configuring saving parameters. Users can customize this class as needed for use in metis methods.

### Parameters:

- `save_image_primary_dir`: The primary directory for saving images.
- `save_image_secondary_dir`: The secondary directory for saving images.
- `save_image_name`: The name of the saved image.
- `is_refresh_screenshot`: Whether to refresh the screenshot.

## Typical steps for using metis are as follows:

1. Create a subclass inheriting from MetisClass.
2. Customize ImageRecognitionParams and SaveParams classes as needed.
3. Implement the required image recognition and manipulation methods in the subclass.
4. Create an instance of the subclass and call the corresponding methods to execute the script.

Please refer to the provided usage example to understand how to use metis in a real project.
