import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metisse.metisse import MetisseClass
from metisse.params import ImageRecognitionParams, SaveParams


class CustomImage(ImageRecognitionParams):
    def __init__(self, *args, template_image_secondary_dir="script_example", **kwargs):
        super().__init__(
            *args, template_image_secondary_dir=template_image_secondary_dir, **kwargs
        )


class CustomSave(SaveParams):
    def __init__(self, *args, save_image_secondary_dir="script_example", **kwargs):
        super().__init__(
            *args, save_image_secondary_dir=save_image_secondary_dir, **kwargs
        )


class script_example(MetisseClass):
    def __init__(
        self, device_id="", relatively_path="", pyqt6_ui_label={}, os_environment=""
    ):
        MetisseClass.__init__(
            self,
            device_id=device_id,
            relatively_path=relatively_path,
            pyqt6_ui_label=pyqt6_ui_label,
            os_environment=os_environment,
        )

    def __call__(self, *args, **kwargs):
        self.check_image_recognition(
            CustomImage(
                screen_image_name="tmp0",
                template_image_name="example_template_hand",
                is_refresh_screenshot=False,
            )
        )  # simulate image recognition hand icon , if you want to use this function on real device , you need to set is_refresh_screenshot=True
        print(f"hand pos = {self._img_recog_result.coordinate}")

        self.execute_time_sleep(1)  # wait 1 second

        self.default_tap(
            ImageRecognitionParams(
                screen_image_name="tmp0",
                template_image_name="example_template_face",
                template_image_secondary_dir="script_example",
                is_refresh_screenshot=False,
            )
        )  # simulate image recognition hand icon , if you want to use this function on real device , you need to set is_refresh_screenshot=True
        self.default_tap(
            CustomImage(
                screen_image_name="tmp0",
                template_image_name="example_template_face",
                is_refresh_screenshot=False,
            )
        )  # simulate image recognition hand icon , if you want to use this function on real device , you need to set is_refresh_screenshot=True

        self.save_screenshot_compression(
            SaveParams(
                save_image_name="save_image",
                save_image_primary_dir="storage",
                save_image_secondary_dir="script_example",
                compression=0.5,
                screenshot_wait_time=1,
                is_save_image_name_add_time=True,
                is_refresh_screenshot=False,
            )
        )
        self.save_screenshot_compression(
            CustomSave(
                save_image_name="save_image",
                save_image_primary_dir="storage",
                compression=0.5,
                screenshot_wait_time=1,
                is_save_image_name_add_time=True,
                is_refresh_screenshot=False,
            )
        )
        self.save_screenshot_compression(
            CustomSave(
                save_image_name="save_image",
                save_image_primary_dir="storage",
                save_image_subdirs=["third", "forth"],
                compression=0.5,
                screenshot_wait_time=1,
                is_save_image_name_add_time=True,
                is_refresh_screenshot=False,
            )
        )
        self.crop_screenshot(
            (288, 260),
            (340, 294),
            SaveParams(
                load_image_primary_dir="temp_image",
                save_image_primary_dir="storage",
                save_image_name="eyes",
                load_image_name="tmp0",
                is_refresh_screenshot=False,
            ),
        )
        self.crop_screenshot(
            (288, 260),
            (340, 294),
            SaveParams(
                load_image_primary_dir="temp_image",
                save_image_primary_dir="temp_image",
                save_image_secondary_dir="crop",
                save_image_name="small_image_tmp",
                load_image_name="tmp0",
                is_refresh_screenshot=False,
            ),
        )
        self.default_tap(
            ImageRecognitionParams(
                screen_image_name="tmp0",
                template_image_name="small_image_tmp",
                template_image_primary_dir="temp_image",
                template_image_secondary_dir="crop",
                is_refresh_screenshot=False,
            )
        )  # simulate image recognition hand icon , if you want to use this function on real device , you need to set is_refresh_screenshot=True


if __name__ == "__main__":
    script_obj = script_example("01234567(test_uid)", None, None, "android")
    script_obj()
