# -*- coding=UTF-8 -*-
# pyright: strict
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple


class Client(ABC):
    """
    template for client
    """

    @abstractmethod
    def screenshot(self, save_screenshot_path: str) -> None:
        """
        take a screenshot
        """
        ...

    @abstractmethod
    def tap(self, coordinates: Tuple[int, int]) -> None:
        """
        tap device
        """
        ...

    @abstractmethod
    def swipe(self, start_coordinates: Tuple[int, int], end_coordinates: Tuple[int, int], swiping_time: int) -> None:
        """
        swipe device
        """
        ...