from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel

from core.settings_handler import read_settings_from_json


class ImageViewer(QMainWindow):
    def __init__(self, image_paths):
        super().__init__()
        self.setWindowTitle('Image Duplicate Finder')
        self.setStyleSheet("background-color: #f3f3f3;")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(self.size())
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        width = read_settings_from_json("preview_width")
        height = read_settings_from_json("preview_height")
        max_images_to_display = read_settings_from_json("max_images_to_display")
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        for i, image_path in enumerate(image_paths):
            if i >= max_images_to_display:
                break
            image_label = QLabel(self)
            pixmap = QPixmap(image_path)

            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            path_label = QLabel(image_path, self)
            path_label.setAlignment(Qt.AlignCenter)

            container_layout = QVBoxLayout()
            container_layout.addWidget(image_label)
            container_layout.addWidget(path_label)

            container_widget = QWidget()
            container_widget.setLayout(container_layout)

            self.layout.addWidget(container_widget)
        self.scroll_area.setWidget(self.widget)
        self.setCentralWidget(self.scroll_area)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint) # TODO: найти как скрыть флаг скрывания
        self.setWindowModality(Qt.ApplicationModal)