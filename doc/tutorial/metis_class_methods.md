# MetisClass Methods Documentation

MetisClass is the primary class in the metis package, providing a set of methods for image recognition and manipulation tasks. Here is a detailed description of the methods available in the MetisClass:

- `check_image_recognition(params: ImageRecognitionParams) -> bool`

  This method checks whether the template image is recognized in the screen image using the provided parameters.

  - `params`: An ImageRecognitionParams object containing the necessary parameters for image recognition.
  - Returns a boolean value indicating whether the template image is recognized.

- `default_tap(params: ImageRecognitionParams, tap_execute_wait_time: float = 0.1, tap_execute_counter_times: int = 1, tap_offset: Tuple[int, int] = (0, 0)) -> bool`

  This method performs a tap operation on the recognized image using the provided parameters.

  - `params`: An ImageRecognitionParams object containing the necessary parameters for image recognition.
  - `tap_execute_wait_time`: The wait time (in seconds) between tap executions (default: 0.1 seconds).
  - `tap_execute_counter_times`: The number of times the tap operation will be executed (default: 1).
  - `tap_offset`: A tuple containing the x and y offsets for the tap operation (default: (0, 0)).
  - Returns a boolean value indicating whether the tap operation was successful.

- `default_swipe(params: ImageRecognitionParams, swipe_offset_position: Tuple[int, int] = (0, 0), swiping_time: int = 300, swipe_execute_counter_times: int = 1, swipe_execute_wait_time: float = 0) -> bool`

  This method performs a swipe operation on the recognized image using the provided parameters.

  - `params`: An ImageRecognitionParams object containing the necessary parameters for image recognition.
  - `swipe_offset_position`: A tuple containing the x and y offsets for the swipe operation (default: (0, 0)).
  - `swiping_time`: The duration (in milliseconds) of the swipe operation (default: 300 ms).
  - `swipe_execute_counter_times`: The number of times the swipe operation will be executed (default: 1).
  - `swipe_execute_wait_time`: The wait time (in seconds) between swipe executions (default: 0 seconds).
  - Returns a boolean value indicating whether the swipe operation was successful.

- `default_press(params: ImageRecognitionParams, pressing_time: int = 300, press_execute_counter_times: int = 1, press_execute_wait_time: float = 0) -> bool`

  This method performs a press operation on the recognized image using the provided parameters.

  - `params`: An ImageRecognitionParams object containing the necessary parameters for image recognition.
  - `pressing_time`: The duration (in milliseconds) of the press operation (default: 300 ms).
  - `press_execute_counter_times`: The number of times the press operation will be executed (default: 1).
  - `press_execute_wait_time`: The wait time (in seconds) between press executions (default: 0 seconds).
  - Returns a boolean value indicating whether the press operation was successful.

- `save_screenshot_compression(params: SaveParams)`

  This method saves a compressed screenshot using the provided parameters.

  - `params`: A SaveParams object containing the necessary parameters for saving a screenshot.

- `crop_screenshot(crop_start: Tuple[int, int], crop_end: Tuple[int, int], params: SaveParams)`

  This method crops and saves a screenshot using the provided parameters.

  - `crop_start`: A tuple containing the x and y coordinates of the starting point  for the crop.

  - `crop_end`: A tuple containing the x and y coordinates of the ending point for the crop.
  - `params`: A SaveParams object containing the necessary parameters for saving a cropped screenshot.
- `tap(coordinate: Tuple[int, int], tap_execute_counter_times: int = 1, tap_execute_wait_time: float = 0.1, tap_offset: Tuple[int, int] = (0, 0))`

  This method performs a tap operation at the specified coordinate.

  - `coordinate`: A tuple containing the x and y coordinates where the tap operation will be performed.
  - `tap_execute_counter_times`: The number of times the tap operation will be executed (default: 1).
  - `tap_execute_wait_time`: The wait time (in seconds) between tap executions (default: 0.1 seconds).
  - `tap_offset`: A tuple containing the x and y offsets for the tap operation (default: (0, 0)).
- `swipe(coordinate: Tuple[int, int], swipe_offset_position: Tuple[int, int] = (0, 0), swiping_time: int = 300, swipe_execute_counter_times: int = 1, swipe_execute_wait_time: float = 0)`

  This method performs a swipe operation at the specified coordinate.

  - `coordinate`: A tuple containing the x and y coordinates where the swipe operation will be performed.
  - `swipe_offset_position`: A tuple containing the x and y offsets for the swipe operation (default: (0, 0)).
  - `swiping_time`: The duration (in milliseconds) of the swipe operation (default: 300 ms).
  - `swipe_execute_counter_times`: The number of times the swipe operation will be executed (default: 1).
  - `swipe_execute_wait_time`: The wait time (in seconds) between swipe executions (default: 0 seconds).
- `press(coordinate: Tuple[int, int], pressing_time: int = 300, press_execute_counter_times: int = 1, press_execute_wait_time: float = 0)`

  This method performs a press operation at the specified coordinate.

  - `coordinate`: A tuple containing the x and y coordinates where the press operation will be performed.
  - `pressing_time`: The duration (in milliseconds) of the press operation (default: 300 ms).
  - `press_execute_counter_times`: The number of times the press operation will be executed (default: 1).
  - `press_execute_wait_time`: The wait time (in seconds) between press executions (default: 0 seconds).
- `execute_time_sleep(wait_time: float = 1)`

  This method introduces a pause in the script execution for the specified duration.

  - `wait_time`: The duration (in seconds) to pause the script execution (default: 1 second).
  
These are the main methods available in the MetisClass for performing various image recognition and manipulation tasks. You can use these methods to interact with the images in your script and perform operations like tapping, swiping, and pressing based on the recognized images.
