import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QIcon

from GUI.top_bar_with_icons import create_top_bar_with_icons


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Duplicate Finder')
        self.setStyleSheet("background-color: #f3f3f3;")
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.showMaximized()
        self.setFixedSize(self.size())
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()

        content_strip = QWidget()
        content_layout = QVBoxLayout()

        self.select_folder_button = QPushButton('Выбрать папку')
        self.select_folder_button.clicked.connect(self.select_folder)

        self.selected_folder_label = QLabel('Выбранная папка: Не выбрана')

        content_layout.addWidget(self.select_folder_button)
        content_layout.addWidget(self.selected_folder_label)

        content_strip.setLayout(content_layout)
        white_strip, grey_strip = create_top_bar_with_icons(self)

        self.layout.addWidget(white_strip)
        self.layout.addWidget(grey_strip)
        self.layout.addWidget(content_strip)

        self.main_widget.setLayout(self.layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        if folder_path:
            self.selected_folder_label.setText(f'Выбранная папка: {folder_path}')
        else:
            self.selected_folder_label.setText('Выбранная папка: Не выбрана')
