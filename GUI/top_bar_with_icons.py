from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolButton, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


def create_top_bar_with_icons(parent_widget):
    white_strip = QWidget(parent_widget)
    white_strip.setStyleSheet("background-color: #f3f3f3;")
    white_strip.setFixedHeight(30)

    grey_strip = QWidget(parent_widget)
    grey_strip.setStyleSheet("background-color: #d7d8da;")
    grey_strip.setFixedHeight(60)
    grey_layout = QHBoxLayout(grey_strip)
    grey_layout.setAlignment(Qt.AlignLeft)

    grey_layout.setSpacing(0)

    add_icon_to_layout(grey_layout, 'assets/iconRun.png', 'Запустить поиск')
    add_icon_to_layout(grey_layout, 'assets/iconHomepage.png', 'Хочу домой')
    add_icon_to_layout(grey_layout, 'assets/iconSettings.png', 'Настройки')
    add_icon_to_layout(grey_layout, 'assets/iconHelp.png', 'Мне нужна помощь')
    add_icon_to_layout(grey_layout, 'assets/iconInformation.png', 'Информация о приложении')

    grey_strip.setLayout(grey_layout)

    return white_strip, grey_strip


def add_icon_to_layout(layout, icon_path, tooltip_text):
    icon_size = QSize(512, 512)

    icon_button = QToolButton()
    icon_button.setIcon(QIcon(icon_path))
    icon_button.setIconSize(icon_size)
    icon_button.setFixedHeight(40)
    icon_button.setFixedWidth(100)
    icon_button.setToolTip(tooltip_text)
    icon_button.setStyleSheet("""
            QToolButton {
                background-color: #d7d8da;
                border: none;
            }
            QToolButton::hover {
                background-color: #d7d8da;
            }
            QToolTip {
                background-color: white;
                color: black;
                border: none;
                font-family: "Times New Roman", Times, serif;
                font-size: 14px;
            }
        """)

    separator_line = QFrame()
    separator_line.setFrameShape(QFrame.VLine)
    separator_line.setFrameShadow(QFrame.Sunken)
    separator_line.setStyleSheet("color: #afb2b7")
    layout.addWidget(icon_button)
    layout.addWidget(separator_line)
