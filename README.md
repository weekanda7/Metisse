# Metis

Metis is a powerful image recognition and automation package designed to facilitate the development of scripts for mobile devices. It provides an extensive set of tools for image recognition, screenshot manipulation, and user interaction, such as tapping, swiping, and pressing.

## Features

- Image recognition using template matching
- Screenshot manipulation, including cropping and saving
- Automation of user interactions, such as tapping, swiping, and pressing
- Customizable parameters for image recognition and automation tasks
- Easy integration with existing automation frameworks

## Installation

To install Metis, run the following command in your terminal:

```bash
pip install metis
```
Usage
Here's a simple example demonstrating how to use Metis for image recognition and user interaction:

python
Copy code
```bash
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from metis.metis import MetisClass
from metis.params import ImageRecognitionParams, SaveParams

class CustomImage(ImageRecognitionParams):
    def __init__(self, *args, template_image_secondary_dir="script_example", **kwargs):
        super().__init__(*args, template_image_secondary_dir=template_image_secondary_dir, **kwargs)

class CustomSave(SaveParams):
    def __init__(self, *args, save_image_secondary_dir="script_example", **kwargs):
        super().__init__(*args, save_image_secondary_dir=save_image_secondary_dir, **kwargs)

class script_example(MetisClass):
    def __init__(self, device_id="", relatively_path="", pyqt6_ui_label={}, os_environment=""):
        MetisClass.__init__(
            self,
            device_id=device_id,
            relatively_path=relatively_path,
            pyqt6_ui_label=pyqt6_ui_label,
            os_environment=os_environment,
        )

    def __call__(self):
        # Your custom script implementation goes here

if __name__ == "__main__":
    script_obj = script_example("test_uid", None, None, "android")
    script_obj()
```
For more detailed information about the available methods and their usage, please refer to the MetisClass Methods documentation.

## Contributing
We welcome contributions to Metis! If you'd like to contribute, please follow these steps:  
- Fork the repository
- Create a new branch for your changes
- Make your changes and test them thoroughly
- Commit your changes and push them to your forked repository
- Create a pull request with a detailed description of your changes
- Please make sure to follow the code style and conventions used in the project.

## License
Metis is licensed under the Apache License 2.0.