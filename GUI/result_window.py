from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QMainWindow, QWidget, QScrollArea, QPushButton, QApplication
import time
from multiprocessing import Process, Queue
from GUI.loading_window import LoadingWindow
from GUI.similar_images_window import run_similar_images_viewer
from GUI.top_bar_with_icons import create_top_bar_with_icons
from core.settings_handler import read_settings_from_json


class ResultsWindow(QMainWindow):
    def __init__(self, main_window, results):
        super().__init__()
        self.viewer_process = None
        self.loading_window = None
        self.main_window = main_window

        self.setWindowTitle('Image Duplicate Finder')
        self.width = read_settings_from_json("preview_width")
        self.height = read_settings_from_json("preview_height")
        self.setStyleSheet("background-color: #f3f3f3;")
        self.setWindowIcon(QIcon('assets/icon.png'))

        screen_geometry = QApplication.desktop().screenGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.setFixedSize(self.screen_width, self.screen_height)
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

        if not results:
            no_results_label = QLabel("Нет подобных изображений")
            no_results_label.setAlignment(Qt.AlignCenter)
            scroll_layout.addWidget(no_results_label)
        else:
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
                view_button.clicked.connect(
                    lambda checked, res=result: self.start_similar_images_loading(res['similar_images']))

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

    def start_similar_images_loading(self, similar_images):
        self.loading_window = LoadingWindow(self)
        self.loading_window.show()
        queue = Queue()

        self.viewer_process = Process(target=run_similar_images_viewer, args=(similar_images, self.width, self.height, queue))
        self.viewer_process.start()

        while True:
            if not queue.empty():
                message = queue.get()
                if message == 'done':
                    self.loading_window.close()
                    break
            time.sleep(0.1)

    def run_homepage(self):
        self.main_window.show()
        self.main_window.showMaximized()
        self.close()
