import pytest

from metisse.clients.client import Client


class DummyClient(Client):
    def screenshot(self, save_screenshot_path: str) -> None:
        return super().screenshot(save_screenshot_path)

    def tap(self, coordinates):
        return super().tap(coordinates)

    def swipe(self, start_coordinates, end_coordinates, swiping_time):
        return super().swipe(start_coordinates, end_coordinates, swiping_time)


def test_client_base_methods_execute():
    dummy = DummyClient()
    assert dummy.screenshot("img.png") is None
    assert dummy.tap((1, 2)) is None
    assert dummy.swipe((1, 1), (2, 2), 100) is None
