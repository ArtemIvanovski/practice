from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QMainWindow, QWidget, QScrollArea, QPushButton

from GUI.loading_window import LoadingDialog
from GUI.top_bar_with_icons import create_top_bar_with_icons
from core.settings_handler import read_settings_from_json
from core.threads.similar_images_processing_thread import SimilarImagesProcessingThread


class ResultsWindow(QMainWindow):
    def __init__(self, main_window, results):
        super().__init__()
        self.similar_images_window_thread = None
        self.loading_dialog = None
        self.similar_images_window = None
        self.main_window = main_window
        self.setWindowTitle('Image Duplicate Finder')
        self.width = read_settings_from_json("preview_width")
        self.height = read_settings_from_json("preview_height")
        self.setStyleSheet("background-color: #f3f3f3;")
        self.setWindowIcon(QIcon('assets/icon.png'))
        # self.setFixedSize(self.size())
        self.main_widget = QWidget()

        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()

        white_strip, grey_strip = create_top_bar_with_icons(self, None, self.run_homepage)
        self.layout.addWidget(white_strip)
        self.layout.addWidget(grey_strip)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        for result in results:
            image_label = QLabel()
            pixmap = QPixmap(result['path']).scaled(self.width, self.height, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            name_label = QLabel(result['path'].split('/')[-1])
            name_label.setAlignment(Qt.AlignCenter)

            count_label = QLabel(f"Подобных изображений: {result['similar_count']}")
            count_label.setAlignment(Qt.AlignCenter)

            view_button = QPushButton("Посмотреть подобные изображения")
            view_button.setFixedSize(350, 30)
            view_button.clicked.connect(lambda checked, res=result: self.view_similar_images(res['similar_images']))

            image_layout = QVBoxLayout()
            image_layout.addStretch()
            image_layout.addWidget(image_label)
            image_layout.addWidget(name_label)
            image_layout.addWidget(count_label)
            image_layout.addWidget(view_button, alignment=Qt.AlignCenter)

            scroll_layout.addLayout(image_layout)

        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)
        self.main_widget.setLayout(self.layout)

    def view_similar_images(self, similar_images):
        self.start_similar_viewer_loading(similar_images)

    def run_homepage(self):
        self.main_window.show()
        self.close()

    def start_similar_viewer_loading(self, similar_images):
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()

        self.similar_images_window_thread = SimilarImagesProcessingThread(similar_images, self.width, self.height)
        self.similar_images_window_thread.finished.connect(self.on_viewer_loaded)
        self.similar_images_window_thread.start()

    def on_similar_viewer_loaded(self, similar_images_window):
        self.loading_dialog.close()
        self.similar_images_window = similar_images_window
        self.similar_images_window.show()
