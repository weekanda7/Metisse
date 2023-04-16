# metis 包说明文档

metis 是一个用于自动化图像识别和操作任务的 Python 库。它提供了一组用户友好的方法，让用户能够使用图像识别技术执行自动点击、滑动和按压操作。以下是 metis 主要功能和用法的简要概述：

## MetisClass

MetisClass 是 metis 中包含所有基本图像识别和操作方法的主要类。要使用 metis，您需要创建一个继承自 MetisClass 的子类并根据需要实现自定义方法。

### 方法：

- `check_image_recognition()`：检查图像识别结果。
- `default_tap()`：在识别到的图像上执行点击操作。
- `default_swipe()`：在识别到的图像上执行滑动操作。
- `default_press()`：在识别到的图像上执行按压操作。
- `save_screenshot_compression()`：保存压缩后的屏幕截图。
- `crop_screenshot()`：裁剪并保存屏幕截图。
- `execute_time_sleep()`：等待指定的时间。

## ImageRecognitionParams

ImageRecognitionParams 是一个用于配置图像识别参数的 dataclass。用户可以根据需要自定义此类以在 metis 方法中使用。

### 参数：

- `template_image_name`：模板图像的名称。
- `compare_times_counter`：图像识别比较次数。
- `screenshot_wait_time`：截取屏幕截图之间的等待时间（以秒为单位）。
- `accuracy_val`：图像识别的准确度值。
- `is_refresh_screenshot`：是否刷新屏幕截图。
- `screen_image_name`：屏幕图像的名称。
- `screen_image_primary_dir`：屏幕图像的主目录。
- `screen_image_secondary_dir`：屏幕图像的次目录。
- `screen_image_subdirs`：屏幕图像的第三层或更高子目录列表。
- `template_image_primary_dir`：模板图像的主目录。
- `template_image_secondary_dir`：模板图像的次目录。
- `template_image_subdirs`：模板图像的第三层或更高子目录列表。
- `is_backup`：是否创建识别图像的备份。
- `repeatedly_screenshot_times`：重复截屏次数。

## SaveParams

SaveParams 是一个用于配置保存参数的 dataclass。用户可以根据需要自定义此类以在 metis 方法中使用。

### 参数：

- `load_image_primary_dir`：加载图像的主目录。
- `save_image_primary_dir`：保存图像的主目录。
- `save_image_name`：保存的图像名称。
- `screenshot_wait_time`：截取屏幕截图之间的等待时间（以秒为单位）。
- `compression`：保存图像的压缩比率。
- `load_image_name`：要加载的图像名称。
- `save_image_secondary_dir`：保存图像的次目录。
- `save_image_subdirs`：保存图像的第三层或更高子目录列表。
- `load_image_secondary_dir`：加载图像的次目录。
- `load_image_subdirs`：加载图像的第三层或更高子目录列表。
- `is_save_image_name_add_time`：是否在保存的图像名称中附加当前时间。
- `is_refresh_screenshot`：是否刷新屏幕截图。

## DeviceParams

DeviceParams 是一个包含与 metis 运行设备相关的参数的 dataclass。这些参数可用于根据设备的规格自定义库的行为。

### 参数：

- `device_id`：表示设备唯一标识符的字符串。
- `os_environment`：表示设备操作系统环境的字符串（例如：“Android”，“Ios”）。

## UiClientParams

UiClientParams 是一个包含与 metis 库用户界面相关的参数的 dataclass。这些参数可用于自定义在 metis 中使用的用户界面元素的外观和行为。

### 参数：

- `image_label`：用于在用户界面中显示图像的 QLabel 对象。
- `log_label`：用于在用户界面中显示日志消息的 QLabel 对象。

## ImageRecognitionResult

ImageRecognitionResult 是一个包含图像识别结果相关信息的类。此类可用于存储和管理由 metis 执行的图像识别操作的结果。

### 属性：

- `is_recognized`：表示图像识别是否成功的布尔值。
- `coordinate`：包含识别图像的 x 和 y 坐标的元组（例如：（x，y））。
- `coordinates_list`：包含所有识别图像的 x 和 y 坐标的元组列表。
- `recognition_threshold`：表示图像识别过程中使用的识别阈值的浮点值。

## 使用 metis 的典型步骤：

1. 创建一个继承自 MetisClass 的子类。
2. 按需要自定义 ImageRecognitionParams 和 SaveParams dataclass。
3. 在子类中实现所需的图像识别和操作方法。
4. 创建子类的实例并调用相应的方法以执行脚本。

请参考提供的使用示例以了解如何在实际项目中使用 metis。