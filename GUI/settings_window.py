from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QWidget, QButtonGroup,
                             QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

from GUI.error_window import ErrorWindow
from core.settings_handler import get_language, write_settings_to_json


class SettingsWindow(QDialog):
    def __init__(self, parent=None, translator_manager=None, app=None, main_window=None, about_window=None, help_window=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.about_window = about_window
        self.help_window = help_window
        self.height_label = None
        self.max_images_label = None
        self.value_columns_label = None
        self.cancel_button = None
        self.width_label = None
        self.translator_manager = translator_manager
        self.main_window = main_window
        self.gif = None
        self.jpeg = None
        self.png = None
        self.bmp = None
        self.language_buttons = None
        self.language_group = None
        self.label_similarity = None
        self.similarity_slider = None
        self.use_d_hash_algorithm = None
        self.use_g_hash_algorithm = None
        self.use_p_hash_algorithm = None
        self.use_a_hash_algorithm = None
        self.warning_label = None
        self.value_columns_input = None
        self.max_images_input = None
        self.height_input = None
        self.width_input = None
        self.setWindowTitle(self.tr("Настройки"))
        self.setGeometry(300, 300, 600, 400)
        self.setFixedSize(self.size())
        main_layout = QVBoxLayout()
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        tabs = QTabWidget()
        tabs.addTab(self.create_general_tab(), self.tr("Основные"))
        tabs.addTab(self.create_comparison_tab(), self.tr("Сравнение"))
        tabs.addTab(self.create_language_tab(), self.tr("Язык"))
        tabs.addTab(self.create_file_formats_tab(), self.tr("Форматы файлов"))

        main_layout.addWidget(tabs)
        main_layout.addLayout(self.create_buttons())

        self.setLayout(main_layout)

    def create_general_tab(self):
        general_tab = QWidget()
        layout = QVBoxLayout()

        width_layout = QHBoxLayout()
        self.width_label = QLabel(self.tr("Ширина превьюшек"))
        from GUI.top_bar_with_icons import create_spin_box
        self.width_input = create_spin_box(1, 10000, "preview_width")
        width_layout.addWidget(self.width_label)
        width_layout.addWidget(self.width_input)

        height_layout = QHBoxLayout()
        self.height_label = QLabel(self.tr("Высота превьюшек"))
        self.height_input = create_spin_box(1, 10000, "preview_height")
        height_layout.addWidget(self.height_label)
        height_layout.addWidget(self.height_input)

        max_images_layout = QHBoxLayout()
        self.max_images_label = QLabel(self.tr("Максимум изображений для вывода в виде превьюшек"))
        self.max_images_input = create_spin_box(2, 10000, "max_images_to_display")
        max_images_layout.addWidget(self.max_images_label)
        max_images_layout.addWidget(self.max_images_input)

        value_columns_layout = QHBoxLayout()
        self.value_columns_label = QLabel(self.tr("Количество столбцов в виде превьюшек"))
        self.value_columns_input = create_spin_box(1, 4, "value_columns")
        value_columns_layout.addWidget(self.value_columns_label)
        value_columns_layout.addWidget(self.value_columns_input)

        layout.addLayout(value_columns_layout)
        layout.addLayout(width_layout)
        layout.addLayout(height_layout)
        layout.addLayout(max_images_layout)
        layout.addStretch(1)

        general_tab.setLayout(layout)
        return general_tab

    def create_comparison_tab(self):
        comparison_tab = QWidget()
        layout = QVBoxLayout()

        self.warning_label = QLabel(self.tr("Внимание: Установка всех этих опций увеличит время сравнения"))
        layout.addWidget(self.warning_label)

        from GUI.top_bar_with_icons import create_checkbox
        self.use_a_hash_algorithm = create_checkbox(self.tr("Использовать алгоритм a-хэширования"), "aHash")
        layout.addWidget(self.use_a_hash_algorithm)

        self.use_p_hash_algorithm = create_checkbox(self.tr("Использовать алгоритм p-хэширования"), "pHash")
        layout.addWidget(self.use_p_hash_algorithm)

        self.use_g_hash_algorithm = create_checkbox(self.tr("Использовать алгоритм g-хэширования"), "gHash")
        layout.addWidget(self.use_g_hash_algorithm)

        self.use_d_hash_algorithm = create_checkbox(self.tr("Использовать алгоритм d-хэширования"), "dHash")
        layout.addWidget(self.use_d_hash_algorithm)

        from GUI.top_bar_with_icons import create_slider
        self.similarity_slider = create_slider(0, 100, "similarity_threshold")
        self.similarity_slider.valueChanged.connect(self.update_label_similarity_text)
        tr_msg = self.tr("Порог сходства: ")
        self.label_similarity = QLabel(tr_msg + str(self.similarity_slider.value()) + " %")
        layout.addWidget(self.label_similarity)
        layout.addWidget(self.similarity_slider)

        comparison_tab.setLayout(layout)
        return comparison_tab

    def update_label_similarity_text(self, value):
        tr_msg = self.tr("Порог сходства: ")
        self.label_similarity.setText(tr_msg + str(value) + " %")

    def create_language_tab(self):
        language_tab = QWidget()
        layout = QVBoxLayout()

        self.language_group = QButtonGroup()
        self.language_buttons = {"en": QRadioButton("English"), "ru": QRadioButton("Русский"),
                                 "be": QRadioButton("Беларускі"), "fr": QRadioButton("Français")}

        for key, button in self.language_buttons.items():
            self.language_group.addButton(button)
            layout.addWidget(button)

        from core.settings_handler import get_language
        self.language_buttons[get_language()].setChecked(True)

        layout.addStretch(1)
        language_tab.setLayout(layout)
        return language_tab

    def create_file_formats_tab(self):
        file_formats_tab = QWidget()
        layout = QVBoxLayout()

        from GUI.top_bar_with_icons import create_checkbox
        self.bmp = create_checkbox(".bmp", "bmp")
        layout.addWidget(self.bmp)

        self.png = create_checkbox(".png", "png")
        layout.addWidget(self.png)

        self.gif = create_checkbox(".gif", "gif")
        layout.addWidget(self.gif)

        self.jpeg = create_checkbox(".jpeg", "jpeg")
        layout.addWidget(self.jpeg)

        layout.addStretch(1)
        file_formats_tab.setLayout(layout)
        return file_formats_tab

    def create_buttons(self):
        button_layout = QHBoxLayout()
        icon_size = QSize(20, 20)
        ok_button = QPushButton("OK")
        ok_button.setIcon(QIcon('assets/iconYes.png'))
        ok_button.setIconSize(icon_size)
        ok_button.setFixedHeight(40)
        ok_button.setFixedWidth(100)

        self.cancel_button = QPushButton(self.tr("Отмена"))
        self.cancel_button.setIcon(QIcon('assets/iconCancel.png'))
        self.cancel_button.setIconSize(icon_size)
        self.cancel_button.setFixedHeight(40)
        self.cancel_button.setFixedWidth(100)

        button_layout.addStretch(1)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(self.cancel_button)

        ok_button.clicked.connect(self.on_ok_button_clicked)
        self.cancel_button.clicked.connect(self.reject)

        return button_layout

    def on_ok_button_clicked(self):
        if not (self.bmp.isChecked() or self.png.isChecked() or self.jpeg.isChecked() or self.gif.isChecked()):
            error_dialog = ErrorWindow(self.tr("Не выбран ни один тип файла"))
            error_dialog.exec_()
            return

        settings = {
            "preview_width": self.width_input.value(),
            "preview_height": self.height_input.value(),
            "max_images_to_display": self.max_images_input.value(),
            "value_columns": self.value_columns_input.value(),
            "similarity_threshold": self.similarity_slider.value(),
            "aHash": self.use_a_hash_algorithm.isChecked(),
            "pHash": self.use_p_hash_algorithm.isChecked(),
            "dHash": self.use_d_hash_algorithm.isChecked(),
            "gHash": self.use_g_hash_algorithm.isChecked(),
            "english": self.language_buttons["en"].isChecked(),
            "russian": self.language_buttons["ru"].isChecked(),
            "french": self.language_buttons["fr"].isChecked(),
            "belarusian": self.language_buttons["be"].isChecked(),
            "bmp": self.bmp.isChecked(),
            "png": self.png.isChecked(),
            "jpeg": self.jpeg.isChecked(),
            "gif": self.gif.isChecked()
        }

        current_language = get_language()
        write_settings_to_json(settings)
        selected_language = None
        for code, button in self.language_buttons.items():
            if button.isChecked():
                selected_language = code
                break

        if selected_language and selected_language != current_language:
            self.translator_manager.change_language(self.app, selected_language)
            self.parent.update_ui_texts()
            self.update_ui_texts()
            self.about_window.update_ui_texts()
            self.help_window.update_ui_texts()
            if self.main_window is not None:
                self.main_window.update_ui_texts()

        self.accept()

    def update_ui_texts(self):
        self.setWindowTitle(self.tr("Настройки"))
        tabs = self.findChild(QTabWidget)
        tabs.setTabText(0, self.tr("Основные"))
        tabs.setTabText(1, self.tr("Сравнение"))
        tabs.setTabText(2, self.tr("Язык"))
        tabs.setTabText(3, self.tr("Форматы файлов"))

        self.width_label.setText(self.tr("Ширина превьюшек"))
        self.height_label.setText(self.tr("Высота превьюшек"))
        self.max_images_label.setText(self.tr("Максимум изображений для вывода в виде превьюшек"))
        self.value_columns_label.setText(self.tr("Количество столбцов в виде превьюшек"))

        self.warning_label.setText(self.tr("Внимание: Установка всех этих опций увеличит время сравнения"))
        self.use_a_hash_algorithm.setText(self.tr("Использовать алгоритм a-хэширования"))
        self.use_p_hash_algorithm.setText(self.tr("Использовать алгоритм p-хэширования"))
        self.use_g_hash_algorithm.setText(self.tr("Использовать алгоритм g-хэширования"))
        self.use_d_hash_algorithm.setText(self.tr("Использовать алгоритм d-хэширования"))
        self.update_label_similarity_text(self.similarity_slider.value())

        self.cancel_button.setText(self.tr("Отмена"))
