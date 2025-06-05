import pytest

from metisse.params import ImageRecognitionParams, SaveParams
from metisse.template_metis import TemplateMetisClass


class DummyTemplate(TemplateMetisClass):
    @property
    def get_device_id(self) -> str:
        return super().get_device_id

    def check_image_recognition(self, params: ImageRecognitionParams) -> bool:
        return super().check_image_recognition(params)

    def screenshot(
        self,
        save_screenshot_name: str,
        save_screenshot_root_key: str,
        save_screenshot_additional_root: str,
    ) -> None:
        return super().screenshot(
            save_screenshot_name,
            save_screenshot_root_key,
            save_screenshot_additional_root,
        )

    def tap(self, center, tap_execute_counter_times, tap_execute_wait_time, tap_offset):
        return super().tap(
            center, tap_execute_counter_times, tap_execute_wait_time, tap_offset
        )

    def default_tap(
        self, params, tap_execute_wait_time, tap_execute_counter_times, tap_offset
    ):
        return super().default_tap(
            params, tap_execute_wait_time, tap_execute_counter_times, tap_offset
        )

    def swipe(
        self,
        center,
        swipe_offset_position,
        swiping_time,
        swipe_execute_counter_times,
        swipe_execute_wait_time,
    ):
        return super().swipe(
            center,
            swipe_offset_position,
            swiping_time,
            swipe_execute_counter_times,
            swipe_execute_wait_time,
        )

    def press(
        self,
        center,
        pressing_time,
        press_execute_counter_times,
        press_execute_wait_time,
    ):
        return super().press(
            center, pressing_time, press_execute_counter_times, press_execute_wait_time
        )

    def save_screenshot_compression(self, save_params: SaveParams) -> None:
        return super().save_screenshot_compression(save_params)

    def crop_screenshot(
        self, coordinate1_tuple1, coordinate2_tuple2, save_params: SaveParams
    ) -> None:
        return super().crop_screenshot(
            coordinate1_tuple1, coordinate2_tuple2, save_params
        )


def test_cannot_instantiate_abstract():
    with pytest.raises(TypeError):
        TemplateMetisClass()


def test_dummy_template_methods_return_none():
    dummy = DummyTemplate()
    assert dummy.get_device_id is None
    assert dummy.check_image_recognition(ImageRecognitionParams()) is None
    assert dummy.screenshot("a", "b", "c") is None
    assert dummy.tap((0, 0), 1, 0.0, (0, 0)) is None
    assert dummy.default_tap(ImageRecognitionParams(), 0.0, 1, (0, 0)) is None
    assert dummy.swipe((0, 0), (1, 1), 10, 1, 0.0) is None
    assert dummy.press((0, 0), 10, 1, 0.0) is None
    assert dummy.save_screenshot_compression(SaveParams()) is None
    assert dummy.crop_screenshot((0, 0), (1, 1), SaveParams()) is None
