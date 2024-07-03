from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStyle
from PyQt5.QtGui import QFont, QPixmap, QIcon


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.setWindowTitle(self.tr('О программе Image Duplicate Finder'))
        self.setFixedSize(550, 600)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        layout = QVBoxLayout()

        logo_pixmap = QPixmap("assets/icon.png")
        logo_label = QLabel()
        logo_pixmap = logo_pixmap.scaled(250, 250, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        title_label = QLabel("Image Duplicate Finder")
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel("Image Duplicate Finder 1.0 Build 5")
        version_font = QFont("Arial", 12)
        version_label.setFont(version_font)
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        copyright_label = QLabel("Copyright https://github.com/ArtemIvanovski.")
        copyright_font = QFont("Arial", 10)
        copyright_label.setFont(copyright_font)
        copyright_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright_label)

        icon_size = QSize(20, 20)
        ok_button = QPushButton("OK")
        ok_button.setIcon(QIcon('assets/iconYes.png'))
        ok_button.setIconSize(icon_size)
        ok_button.setFixedHeight(40)
        ok_button.setFixedWidth(100)
        ok_button.clicked.connect(self.accept)
        ok_button_layout = QHBoxLayout()
        ok_button_layout.addStretch()
        ok_button_layout.addWidget(ok_button)
        ok_button_layout.addStretch()
        layout.addLayout(ok_button_layout)

        self.setLayout(layout)
