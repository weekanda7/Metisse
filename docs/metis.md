# metisse Package Documentation

metisse is a Python library for automating image recognition and manipulation tasks. It provides a set of user-friendly methods that allow users to perform automated tapping, swiping, and pressing operations using image recognition techniques. Below is a brief overview of the main features and usage of metisse:

## MetisseClass

MetisseClass is the primary class in metisse containing all the basic image recognition and manipulation methods. To use metisse, you need to create a subclass inheriting from MetisseClass and implement custom methods as needed.

### Methods:

- `check_image_recognition()`: Checks the image recognition results.
- `default_tap()`: Performs a tap operation on the recognized image.
- `default_swipe()`: Performs a swipe operation on the recognized image.
- `default_press()`: Performs a press operation on the recognized image.
- `save_screenshot_compression()`: Saves a compressed screenshot.
- `crop_screenshot()`: Crops and saves a screenshot.
- `execute_time_sleep()`: Waits for a specified amount of time.

## ImageRecognitionParams

ImageRecognitionParams is a dataclass for configuring image recognition parameters. Users can customize this class as needed for use in metisse methods.

### Parameters:

- `template_image_name`: The name of the template image.
- `compare_times_counter`: The number of times to compare images for recognition.
- `screenshot_wait_time`: The waiting time between taking screenshots (in seconds).
- `accuracy_val`: The accuracy value for image recognition.
- `is_refresh_screenshot`: Whether to refresh the screenshot.
- `screen_image_name`: The name of the screen image.
- `screen_image_primary_dir`: The primary directory of the screen image.
- `screen_image_secondary_dir`: The secondary directory of the screen image.
- `screen_image_subdirs`: The list of third-level or higher subdirectories for the screen image.
- `template_image_primary_dir`: The primary directory of the template image.
- `template_image_secondary_dir`: The secondary directory of the template image.
- `template_image_subdirs`: The list of third-level or higher subdirectories for the template image.
- `is_backup`: Whether to create a backup of the recognized image.
- `repeatedly_screenshot_times`: The number of times to take screenshots repeatedly.

## SaveParams

SaveParams is a dataclass for configuring saving parameters. Users can customize this class as needed for use in metisse methods.

### Parameters:

- `load_image_primary_dir`: The primary directory for loading images.
- `save_image_primary_dir`: The primary directory for saving images.
- `save_image_name`: The name of the saved image.
- `screenshot_wait_time`: The waiting time between taking screenshots (in seconds).
- `compression`: The compression ratio for saved images.
- `load_image_name`: The name of the image to be loaded.
- `save_image_secondary_dir`: The secondary directory for saving images.
- `save_image_subdirs`: The list of third-level or higher subdirectories for saving images.
- `load_image_secondary_dir`: The secondary directory for loading images.
- `load_image_subdirs`: The list of third-level or higher subdirectories for loading images.
- `is_save_image_name_add_time`: Whether to append the current time to the saved image name.
- `is_refresh_screenshot`: Whether to refresh the screenshot.

## DeviceParams

DeviceParams is a dataclass containing parameters related to the device on which metisse is running. These parameters can be used to customize the behavior of the library according to the device's specifications.

### Parameters:

- `device_id`: A string representing the unique identifier of the device.
- `os_environment`: A string representing the operating system environment of the device (e.g., "Android", "Ios").

## UiClientParams

UiClientParams is a dataclass containing parameters related to the user interface of the metisse library. These parameters can be used to customize the appearance and behavior of the user interface elements used in metisse.

### Parameters:

- `image_label`: A QLabel object used to display images in the user interface.
- `log_label`: A QLabel object used to display log messages in the user interface.

## ImageRecognitionResult

ImageRecognitionResult is a class containing information related to the image recognition result. This class can be used to store and manage the results of image recognition operations performed by metisse.

### Attributes:

- `is_recognized`: A boolean value indicating whether the image recognition was successful.
- `coordinate`: A tuple containing the x and y coordinates of the recognized image (e.g., (x, y)).
- `coordinates_list`: A list of tuples containing the x and y coordinates of all recognized images.
- `recognition_threshold`: A float value representing the recognition threshold used in the image recognition process.

## Typical steps for using metisse are as follows:

1. Create a subclass inheriting from MetisseClass.
2. Customize ImageRecognitionParams and SaveParams dataclasses as needed.
3. Implement the required image recognition and manipulation methods in the subclass.
4. Create an instance of the subclass and call the corresponding methods to execute the script.

Please refer to the provided usage example to understand how to use metisse in a real project.