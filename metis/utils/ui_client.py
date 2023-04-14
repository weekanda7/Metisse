from ..params import UiClientParams
from PyQt6.QtGui import QImage, QPixmap
import cv2


class UiClient(object):

    def __init__(self, ui_client_params: UiClientParams) -> None:
        self.ui_client_params = ui_client_params

    def send_log_to_ui(self, _log_message: str):
        if self.ui_client_params and self.ui_client_params.log_label:
            self.ui_client_params.log_label.setText(_log_message)

    def send_image_path_to_ui(self, _image_path: str):
        if self.ui_client_params and self.ui_client_params.image_label:
            self._pyqt_img = cv2.imread(_image_path)
            _height, _width, _ = self._pyqt_img.shape
            _bytes_perline = 3 * _width
            self.qimg = QImage(
                self._pyqt_img,  # type: ignore
                _width,
                _height,
                _bytes_perline,  # type: ignore
                QImage.Format.Format_RGB888).rgbSwapped()  # type: ignore
            self.ui_client_params.image_label.setPixmap(QPixmap.fromImage(self.qimg))