# -*- coding=UTF-8 -*-

from typing import List, Tuple
from mss import mss
import win32api
import win32con
import win32gui
from PIL import Image
import pygetwindow as gw
import time
from ..client import Client
from ...params import DeviceParams

class WindowsClient(Client):
    def __init__(self, device_params: DeviceParams , screen_size: Tuple[int, int]=(640, 1080)):
        assert device_params.os_environment == 'windows', 'device_params.os_environment must be windows'
        self.device_params = device_params
        self.window_title = device_params.device_id
        self.hwnd = win32gui.FindWindow(None, self.window_title)
        self.target_window = gw.getWindowsWithTitle(self.window_title)[0]
        self.target_window.restore()  # 将窗口恢复到正常状态（即非最小化状态）
        self.target_window.moveTo(0, 0)  # 将窗口移动到屏幕的 (0, 0) 坐标
        self.target_window.resizeTo(screen_size[0], screen_size[1])  # 将窗口调整为 (640, 1080) 大小
    @staticmethod
    def get_title() -> List[List[str]]:
        title_list = []
        def callback(hwnd, titles):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title:
                    titles.append((hwnd, window_title))
        titles = []
        win32gui.EnumWindows(callback, titles)

        for hwnd, title in titles:
            title_list.append([f"Handle: {hwnd}, Title: {title}"])
        return title_list

    def resize(self, screen_size: Tuple[int, int]=(640, 1080)) -> None:
        self.target_window.resizeTo(screen_size[0], screen_size[1])

    def screenshot(self, save_screenshot_path: str) -> None:
        self.set_front()  # 确保窗口在前景
        with mss() as sct:
            window_rect = win32gui.GetWindowRect(self.target_window._hWnd)
            monitor = {"top": window_rect[1], "left": window_rect[0], "width": window_rect[2] - window_rect[0], "height": window_rect[3] - window_rect[1]}
            img = sct.grab(monitor)
            img_pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            img_pil.save(save_screenshot_path,dpi=(90, 90))

    def tap(self, coordinates: Tuple[int, int]) -> None:
        self.set_front()
        x, y = coordinates
        hWnd = self.target_window._hWnd
        client_rect = win32gui.GetClientRect(hWnd)
        window_rect = win32gui.GetWindowRect(hWnd)
        border_thickness = int((window_rect[2] - window_rect[0] - client_rect[2]) / 2)
        title_bar_height = window_rect[3] - window_rect[1] - client_rect[3] - border_thickness
        print(window_rect[0],window_rect[1])
        print(border_thickness,title_bar_height)
        adjusted_x = x + window_rect[0] + border_thickness
        adjusted_y = y + window_rect[1] # title_bar_height
        win32api.SetCursorPos((adjusted_x, adjusted_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def swipe(self, start_coordinates: Tuple[int, int], end_coordinates: Tuple[int, int], swiping_time: int) -> None:
        self.set_front()
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates
        hWnd = self.target_window._hWnd
        client_rect = win32gui.GetClientRect(hWnd)
        window_rect = win32gui.GetWindowRect(hWnd)
        border_thickness = int((window_rect[2] - window_rect[0] - client_rect[2]) / 2)
        title_bar_height = window_rect[3] - window_rect[1] - client_rect[3] - border_thickness

        adjusted_start_x = start_x + window_rect[0] + border_thickness
        adjusted_start_y = start_y + window_rect[1] + title_bar_height
        adjusted_end_x = end_x + window_rect[0] + border_thickness
        adjusted_end_y = end_y + window_rect[1] + title_bar_height

        win32api.SetCursorPos((adjusted_start_x, adjusted_start_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(swiping_time / 1000.0)
        win32api.SetCursorPos((adjusted_end_x, adjusted_end_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def _client_to_screen(self, coordinates: Tuple[int, int]) -> Tuple[int, int]:
        return win32gui.ClientToScreen(self.hwnd, coordinates)
    def set_front(self) -> None:
        """
        Bring the target window to the front
        """
        win32gui.SetForegroundWindow(self.target_window._hWnd)
        time.sleep(0.5)