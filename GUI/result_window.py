from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QMainWindow, QWidget

from GUI.top_bar_with_icons import create_top_bar_with_icons
from core.find_duplicate import find_duplicate


class ResultsWindow(QMainWindow):
    def __init__(self, main_window, image_paths_above, image_paths_below):
        super().__init__()
        self.main_window = main_window
        self.image_paths_above = image_paths_above
        self.image_paths_below = image_paths_below
        self.setWindowTitle('Image Duplicate Finder')
        self.setStyleSheet("background-color: #f3f3f3;")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.showMaximized()
        # TODO: fix fixed size
        # self.setFixedSize(self.size())
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.viewer_window = None

        white_strip, grey_strip = create_top_bar_with_icons(self, None, self.run_homepage)
        self.layout.addWidget(white_strip)
        self.layout.addWidget(grey_strip)
        self.layout.addWidget(white_strip)
        self.layout.addWidget(white_strip)
        self.layout.addWidget(white_strip)
        self.layout.addWidget(white_strip)

        content_strip = QWidget()
        self.layout.addWidget(content_strip)
        find_duplicate(image_paths_above, image_paths_below)

        self.main_widget.setLayout(self.layout)

    def run_homepage(self):
        self.main_window.show()
        self.close()
