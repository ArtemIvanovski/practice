from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QWidget, QButtonGroup,
                             QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

from GUI.error_window import ErrorWindow


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setGeometry(300, 300, 600, 600)
        self.setFixedSize(self.size())
        main_layout = QVBoxLayout()
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        tabs = QTabWidget()
        tabs.addTab(self.create_general_tab(), "Основные")
        tabs.addTab(self.create_comparison_tab(), "Сравнение")
        tabs.addTab(self.create_language_tab(), "Язык")
        tabs.addTab(self.create_file_formats_tab(), "Форматы файлов")

        main_layout.addWidget(tabs)
        main_layout.addLayout(self.create_buttons())

        self.setLayout(main_layout)

    def create_general_tab(self):
        general_tab = QWidget()
        layout = QVBoxLayout()

        width_layout = QHBoxLayout()
        width_label = QLabel("Ширина превьюшек")
        from GUI.top_bar_with_icons import create_spin_box
        self.width_input = create_spin_box(1, 10000, "preview_width")
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_input)

        height_layout = QHBoxLayout()
        height_label = QLabel("Высота превьюшек")
        self.height_input = create_spin_box(1, 10000, "preview_height")
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_input)

        max_images_layout = QHBoxLayout()
        max_images_label = QLabel("Максимум изображений для вывода в виде превьюшек")
        self.max_images_input = create_spin_box(2, 10000, "max_images_to_display")
        max_images_layout.addWidget(max_images_label)
        max_images_layout.addWidget(self.max_images_input)

        value_columns_layout = QHBoxLayout()
        value_columns_label = QLabel("Количество столбцов в виде превьюшек")
        self.value_columns_input = create_spin_box(1, 5, "value_columns")
        value_columns_layout.addWidget(value_columns_label)
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

        group_box = QWidget()
        group_layout = QVBoxLayout()

        from GUI.top_bar_with_icons import create_checkbox
        self.rotate_90 = create_checkbox("Поворот 90° по часовой", "rotate_90_clockwise")
        group_layout.addWidget(self.rotate_90)
        self.rotate_180 = create_checkbox("Поворот 180°", "rotate_180")
        group_layout.addWidget(self.rotate_180)
        self.rotate_270 = create_checkbox("Поворот 270° по часовой", "rotate_270_clockwise")
        group_layout.addWidget(self.rotate_270)
        self.flip_horizontal = create_checkbox("Отражение по горизонтали", "flip_horizontal")
        group_layout.addWidget(self.flip_horizontal)
        self.flip_vertical = create_checkbox("Отражение по вертикали", "flip_vertical")
        group_layout.addWidget(self.flip_vertical)

        self.warning_label = QLabel("Внимание: Установка этих опций увеличит время сравнения")
        group_layout.addWidget(self.warning_label)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        self.use_a_hash_algorithm = create_checkbox("Использовать алгоритм a-хэширования", "aHash")
        layout.addWidget(self.use_a_hash_algorithm)

        self.use_p_hash_algorithm = create_checkbox("Использовать алгоритм p-хэширования", "aHash")
        layout.addWidget(self.use_p_hash_algorithm)

        self.use_g_hash_algorithm = create_checkbox("Использовать алгоритм g-хэширования", "aHash")
        layout.addWidget(self.use_g_hash_algorithm)

        self.use_d_hash_algorithm = create_checkbox("Использовать алгоритм d-хэширования", "aHash")
        layout.addWidget(self.use_d_hash_algorithm)


        self.use_sector_algorithm = create_checkbox("Использовать алгоритм сравнения по секторам",
                                                    "use_sector_algorithm")
        layout.addWidget(self.use_sector_algorithm)

        from GUI.top_bar_with_icons import create_slider
        self.similarity_slider = create_slider(0, 100, "similarity_threshold")
        self.similarity_slider.valueChanged.connect(self.update_label_similarity_text)
        self.label_similarity = QLabel(f"Порог сходства: {self.similarity_slider.value()} %")
        layout.addWidget(self.label_similarity)
        layout.addWidget(self.similarity_slider)

        self.sector_slider = create_slider(2, 20, "number_of_sectors")
        self.sector_slider.valueChanged.connect(self.update_label_sector_text)
        self.label_sector = QLabel(f"Количество секторов: {self.sector_slider.value()}")

        layout.addWidget(self.label_sector)
        layout.addWidget(self.sector_slider)

        comparison_tab.setLayout(layout)
        return comparison_tab

    def update_label_similarity_text(self, value):
        self.label_similarity.setText(f"Порог сходства: {value} %")

    def update_label_sector_text(self, value):
        self.label_sector.setText(f"Количество секторов: {value} ")

    def create_language_tab(self):
        language_tab = QWidget()
        layout = QVBoxLayout()

        self.language_group = QButtonGroup()
        self.language_buttons = {}

        self.language_buttons["english"] = QRadioButton("English")
        self.language_buttons["russian"] = QRadioButton("Русский")
        self.language_buttons["belarusian"] = QRadioButton("Беларускі")
        self.language_buttons["french"] = QRadioButton("Français")

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

        cancel_button = QPushButton("Отмена")
        cancel_button.setIcon(QIcon('assets/iconCancel.png'))
        cancel_button.setIconSize(icon_size)
        cancel_button.setFixedHeight(40)
        cancel_button.setFixedWidth(100)

        button_layout.addStretch(1)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        ok_button.clicked.connect(self.on_ok_button_clicked)
        cancel_button.clicked.connect(self.reject)

        return button_layout

    def on_ok_button_clicked(self):

        if not (self.bmp.isChecked() or self.png.isChecked() or self.jpeg.isChecked() or self.gif.isChecked()):
            error_dialog = ErrorWindow("Не выбран ни один тип файла")
            error_dialog.exec_()
            return

        settings = {
            "preview_width": self.width_input.value(),
            "preview_height": self.height_input.value(),
            "max_images_to_display": self.max_images_input.value(),
            "value_columns": self.value_columns_input.value(),
            "similarity_threshold": self.similarity_slider.value(),
            "number_of_sectors": self.sector_slider.value(),
            "rotate_90_clockwise": self.rotate_90.isChecked(),
            "rotate_180": self.rotate_180.isChecked(),
            "rotate_270_clockwise": self.rotate_270.isChecked(),
            "flip_horizontal": self.flip_horizontal.isChecked(),
            "flip_vertical": self.flip_vertical.isChecked(),
            "aHash": self.use_a_hash_algorithm.isChecked(),
            "pHash": self.use_p_hash_algorithm.isChecked(),
            "dHash": self.use_d_hash_algorithm.isChecked(),
            "gHash": self.use_g_hash_algorithm.isChecked(),
            "use_sector_algorithm": self.use_sector_algorithm.isChecked(),
            "english": self.language_buttons["english"].isChecked(),
            "russian": self.language_buttons["russian"].isChecked(),
            "french": self.language_buttons["french"].isChecked(),
            "belarusian": self.language_buttons["belarusian"].isChecked(),
            "bmp": self.bmp.isChecked(),
            "png": self.png.isChecked(),
            "jpeg": self.jpeg.isChecked(),
            "gif": self.gif.isChecked()
        }

        from core.settings_handler import write_settings_to_json
        write_settings_to_json(settings)

        self.accept()
