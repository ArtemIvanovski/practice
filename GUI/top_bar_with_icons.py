from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolButton, QFrame, QCheckBox, QSlider, QSpinBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from GUI.about_window import AboutWindow
from GUI.help_window import HelpWindow
from GUI.settings_window import SettingsWindow
from core.settings_handler import read_settings_from_json


def create_button(text, icon_path, icon_size=QSize(100, 100)):
    button = QPushButton()
    button.setStyleSheet("""
        QPushButton {
            background-color: #afb2b7;
        }
    """)
    button.setFixedSize(QSize(400, 200))
    button.setIconSize(icon_size)
    button.setIcon(QIcon(icon_path))
    button.setText(text)
    return button


def create_checkbox(label_text, setting_key):
    checkbox = QCheckBox(label_text)
    if read_settings_from_json(setting_key):
        checkbox.setCheckState(Qt.Checked)
    return checkbox


def create_slider(min_board, max_board, setting_key):
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_board)
    slider.setMaximum(max_board)
    slider.setValue(read_settings_from_json(setting_key))
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    return slider


def create_spin_box(min_board, max_board, setting_key):
    spin_box = QSpinBox()
    spin_box.setRange(min_board, max_board)
    spin_box.setValue(read_settings_from_json(setting_key))
    return spin_box


def create_top_bar_with_icons(parent_widget, run_search_callback, run_home_comeback):
    white_strip = QWidget(parent_widget)
    white_strip.setStyleSheet("background-color: #f3f3f3;")
    white_strip.setFixedHeight(30)

    grey_strip = QWidget(parent_widget)
    grey_strip.setStyleSheet("background-color: #d7d8da;")
    grey_strip.setFixedHeight(60)
    grey_layout = QHBoxLayout(grey_strip)
    grey_layout.setAlignment(Qt.AlignLeft)

    grey_layout.setSpacing(0)
    about_window = AboutWindow(parent_widget)
    setting_window = SettingsWindow(parent_widget)
    help_window = HelpWindow(parent_widget)

    add_icon_to_layout(grey_layout, 'assets/iconHomepage.png', 'Хочу домой', run_home_comeback)
    add_icon_to_layout(grey_layout, 'assets/iconRun.png', 'Запустить поиск', run_search_callback)
    add_icon_to_layout(grey_layout, 'assets/iconSettings.png', 'Настройки', setting_window.show)
    add_icon_to_layout(grey_layout, 'assets/iconHelp.png', 'Мне нужна помощь', help_window.show)
    add_icon_to_layout(grey_layout, 'assets/iconInformation.png', 'Информация о приложении', about_window.show)

    grey_strip.setLayout(grey_layout)

    return white_strip, grey_strip


def add_icon_to_layout(layout, icon_path, tooltip_text, on_click=None):
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

    if on_click:
        icon_button.clicked.connect(on_click)

    layout.addWidget(icon_button)
    layout.addWidget(separator_line)
