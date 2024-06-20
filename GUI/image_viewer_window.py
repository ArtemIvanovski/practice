from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel, QGridLayout

from core.settings_handler import read_settings_from_json


class ImageViewer(QMainWindow):
    def __init__(self, image_paths):
        super().__init__()
        self.setWindowTitle('Image Duplicate Finder')
        self.setStyleSheet("background-color: #f3f3f3;")
        self.setWindowIcon(QIcon('assets/icon.png'))
        width = read_settings_from_json("preview_width")
        height = read_settings_from_json("preview_height")
        max_images_to_display = read_settings_from_json("max_images_to_display")
        value_columns = read_settings_from_json("value_columns")
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.widget = QWidget()
        self.grid_layout = QGridLayout(self.widget)

        column = 0
        row = 0

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

            container_widget = QWidget()
            container_layout = QVBoxLayout(container_widget)
            container_layout.addWidget(image_label)
            container_layout.addWidget(path_label)
            container_widget.setLayout(container_layout)

            self.grid_layout.addWidget(container_widget, row, column)

            column += 1
            if column >= value_columns:
                column = 0
                row += 1

        self.scroll_area.setWidget(self.widget)
        self.setCentralWidget(self.scroll_area)

        window_width = width * value_columns + 40 * (value_columns + 1)
        # TODO: сделать высоту экранную динамическую
        # window_height = height * ((len(image_paths) - 1) // value_columns + 1) + 80

        self.resize(window_width, 800)
