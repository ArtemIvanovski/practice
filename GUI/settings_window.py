from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
                             QPushButton, QTabWidget, QWidget, QSpinBox, QSlider)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setGeometry(300, 300, 600, 400)

        main_layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(self.create_general_tab(), "Основные")
        tabs.addTab(self.create_comparison_tab(), "Сравнение")
        tabs.addTab(self.create_language_tab(), "Language")
        tabs.addTab(self.create_file_formats_tab(), "Форматы файлов")

        main_layout.addWidget(tabs)
        main_layout.addLayout(self.create_buttons())

        self.setLayout(main_layout)

    def create_general_tab(self):
        general_tab = QWidget()
        layout = QVBoxLayout()

        width_layout = QHBoxLayout()
        width_label = QLabel("Ширина превьюшек")
        self.width_input = QSpinBox()
        self.width_input.setRange(1, 10000)
        self.width_input.setValue(200)
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_input)

        height_layout = QHBoxLayout()
        height_label = QLabel("Высота превьюшек")
        self.height_input = QSpinBox()
        self.height_input.setRange(1, 10000)
        self.height_input.setValue(200)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_input)

        max_images_layout = QHBoxLayout()
        max_images_label = QLabel("Максимум изображений для вывода в виде превьюшек")
        self.max_images_input = QSpinBox()
        self.max_images_input.setRange(1, 10000)
        self.max_images_input.setValue(5000)
        max_images_layout.addWidget(max_images_label)
        max_images_layout.addWidget(self.max_images_input)

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
        self.rotate_180 = QCheckBox("Поворот 180°")
        group_layout.addWidget(self.rotate_180)
        self.rotate_270 = QCheckBox("Поворот 270° по часовой")
        group_layout.addWidget(self.rotate_270)
        self.flip_horizontal = QCheckBox("Отражение по горизонтали")
        group_layout.addWidget(self.flip_horizontal)
        self.flip_vertical = QCheckBox("Отражение по вертикали")
        group_layout.addWidget(self.flip_vertical)

        self.warning_label = QLabel("Внимание: Установка этих опций увеличит время сравнения")
        group_layout.addWidget(self.warning_label)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        self.use_hash_algorithm = create_checkbox("Использовать алгоритм хэширования", "use_hashing_algorithm")
        layout.addWidget(self.use_hash_algorithm)

        self.use_sector_algorithm = create_checkbox("Использовать алгоритм сравнения по секторам", "use_vector_algorithm")
        layout.addWidget(self.use_sector_algorithm)

        self.label_similarity = QLabel("Порог сходства: 95 %")
        layout.addWidget(self.label_similarity)
        self.similarity_slider = QSlider(Qt.Horizontal)
        self.similarity_slider.setMinimum(0)
        self.similarity_slider.setMaximum(100)
        self.similarity_slider.setValue(95)
        self.similarity_slider.setTickInterval(1)
        self.similarity_slider.setTickPosition(QSlider.TicksBelow)
        self.similarity_slider.valueChanged.connect(self.update_label_similarity_text)
        layout.addWidget(self.similarity_slider)

        self.label_sector = QLabel("Количество секторов: 8")
        layout.addWidget(self.label_sector)
        self.sector_slider = QSlider(Qt.Horizontal)
        self.sector_slider.setMinimum(2)
        self.sector_slider.setMaximum(20)
        self.sector_slider.setValue(8)
        self.sector_slider.setTickInterval(1)
        self.sector_slider.setTickPosition(QSlider.TicksBelow)
        self.sector_slider.valueChanged.connect(self.update_label_sector_text)
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
        from GUI.top_bar_with_icons import create_checkbox
        self.language_english = create_checkbox("English", "english")
        layout.addWidget(self.language_english)

        self.language_russian = create_checkbox("Русский", "russian")
        layout.addWidget(self.language_russian)

        self.language_belarussian = create_checkbox("Беларускі", "belarusian")
        layout.addWidget(self.language_belarussian)

        self.language_france = create_checkbox("Français", "french")
        layout.addWidget(self.language_france)

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

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        return button_layout
