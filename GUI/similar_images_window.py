import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QApplication

from core.settings_handler import read_settings_from_json


class SimilarImagesWindow(QMainWindow):
    def __init__(self, similar_images, width, height):
        super().__init__()
        self.similar_images = similar_images
        self.setWindowTitle('Image Duplicate Finder')
        self.setStyleSheet("background-color: #f3f3f3;")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setGeometry(100, 100, 800, 600)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.main_widget = QWidget()
        scroll_area.setWidget(self.main_widget)
        self.grid_layout = QGridLayout(self.main_widget)

        value_columns = read_settings_from_json("value_columns")
        max_images_to_display = read_settings_from_json("max_images_to_display")
        column = 0
        row = 0

        for i, sim_img in enumerate(self.similar_images):
            if i >= max_images_to_display:
                break
            image_label = QLabel()
            pixmap = QPixmap(sim_img['path']).scaled(width, height, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            name_label = QLabel(sim_img['path'].split('/')[-1])
            name_label.setAlignment(Qt.AlignCenter)

            similarity_label = QLabel(f"Коэффициент подобия: {sim_img['similarity']}%")
            similarity_label.setAlignment(Qt.AlignCenter)

            container_widget = QWidget()
            container_layout = QVBoxLayout(container_widget)
            container_layout.addWidget(image_label)
            container_layout.addWidget(name_label)
            container_layout.addWidget(similarity_label)
            container_widget.setLayout(container_layout)

            self.grid_layout.addWidget(container_widget, row, column)

            column += 1
            if column >= value_columns:
                column = 0
                row += 1

        self.setCentralWidget(scroll_area)
        window_width = width * value_columns + 40 * (value_columns + 1)
        self.resize(window_width, 800)


def run_similar_images_viewer(similar_images, width, height, queue):
    app = QApplication(sys.argv)
    viewer = SimilarImagesWindow(similar_images, width, height)
    viewer.show()
    queue.put('done')
    sys.exit(app.exec_())
