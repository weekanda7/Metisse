# -*- coding=UTF-8 -*-
# pyright: strict

import cv2
from cv2 import Mat


class Opencv_utils(object):
    """
    image similarity calculation
    """

    def __init__(self, screen_image_path: str, template_image_path: str) -> None:
        self.screen_image_path = screen_image_path
        self.template_image_path = template_image_path
        self.screen_image_mat: Mat
        self.template_image_mat: Mat
        self._set_screen_image_imread_cv2()
        self._set_template_image_imread_cv2()

    def _set_screen_image_imread_cv2(self) -> None:
        self.screen_image_mat = cv2.imread(self.screen_image_path)

    def _set_template_image_imread_cv2(self) -> None:
        self.template_image_mat = cv2.imread(self.template_image_path)
