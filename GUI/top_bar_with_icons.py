from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolButton, QFrame, QCheckBox, QSlider, QSpinBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from GUI.about_window import AboutWindow
from GUI.help_window import HelpWindow
from GUI.settings_window import SettingsWindow
from core.settings_handler import read_settings_from_json, get_language


def create_button(text, icon_path, icon_size=QSize(100, 100)):
    """
    This function creates a QPushButton with custom style, size, icon, and text.

    Parameters:
    text (str): The text to be displayed on the button.
    icon_path (str): The path to the icon image file.
    icon_size (QSize, optional): The size of the icon. Default is QSize(100, 100).

    Returns:
    QPushButton: The created button with the specified properties.
    """
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
    """
    This function creates a QCheckBox with the specified label text and initializes its state based on the setting key.

    Parameters:
    label_text (str): The text to be displayed on the checkbox.
    setting_key (str): The key to read the setting value from the JSON settings file.

    Returns:
    QCheckBox: The created checkbox with the specified properties. The checkbox is checked if the corresponding setting value is True, otherwise it is unchecked.
    """
    checkbox = QCheckBox(label_text)
    if read_settings_from_json(setting_key):
        checkbox.setCheckState(Qt.Checked)
    return checkbox


def create_slider(min_board, max_board, setting_key):
    """
    This function creates a horizontal QSlider with specified minimum and maximum values,
    and initializes its value based on the setting key.

    Parameters:
    min_board (int): The minimum value of the slider.
    max_board (int): The maximum value of the slider.
    setting_key (str): The key to read the setting value from the JSON settings file.

    Returns:
    QSlider: The created slider with the specified properties. The slider's value is set to the corresponding setting value.

    Note:
    The slider's tick interval is set to 1, and the tick position is set to QSlider.TicksBelow.
    """
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_board)
    slider.setMaximum(max_board)
    slider.setValue(read_settings_from_json(setting_key))
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    return slider


def create_spin_box(min_board, max_board, setting_key):
    """
    This function creates a QSpinBox with specified minimum and maximum values,
    and initializes its value based on the setting key.

    Parameters:
    min_board (int): The minimum value of the spin box.
    max_board (int): The maximum value of the spin box.
    setting_key (str): The key to read the setting value from the JSON settings file.

    Returns:
    QSpinBox: The created spin box with the specified properties. The spin box's value is set to the corresponding setting value.

    Note:
    The spin box's step size is set to 1 be default.
    """
    spin_box = QSpinBox()
    spin_box.setRange(min_board, max_board)
    spin_box.setValue(read_settings_from_json(setting_key))
    return spin_box


def create_top_bar_with_icons(parent_widget, run_search_callback, run_home_comeback, translator_manager, app,
                              main_window):
    """
    This function creates a top bar with icons for different functionalities.

    Parameters:
    parent_widget (QWidget): The parent widget for the top bar.
    run_search_callback (function): The callback function to be executed when the "Run Search" icon is clicked.
    run_home_comeback (function): The callback function to be executed when the "Home" icon is clicked.

    Returns:
    tuple: A tuple containing three elements:
            - A white strip (QWidget)
            - A grey strip with icons (QWidget)
            - A list of QToolButton objects representing the icons/buttons
    """
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
    help_window = HelpWindow(parent_widget)
    setting_window = SettingsWindow(parent_widget, translator_manager, app, main_window, about_window, help_window)
    buttons = []
    text_translate = ['Хочу домой', 'Запустить поиск', 'Настройки', 'Мне нужна помощь', 'Информация о приложении']

    code_language = get_language()

    if code_language == 'en':
        text_translate = ['Go home', 'Start the search', 'Settings', 'I need help', 'Information about the application']
    elif code_language == 'be':
        text_translate = ['Жадаю дадому', 'Запусціць пошук', 'Налады', 'Мне патрэбна дапамога', 'Інфармацыя аб праграме']
    elif code_language == 'fr':
        text_translate = ['Je veux rentrer à la maison', 'Lancer la recherche', 'Réglages', 'Jai besoin daide', 'Informations sur lapplication']

    def add_icon_to_layout(layout, icon_path, tooltip_text, on_click=None):
        """
        This function adds an icon button and a vertical separator line to a given layout.

        Parameters:
        layout (QHBoxLayout): The layout to which the icon button and separator line will be added.
        icon_path (str): The path to the icon image file.
        tooltip_text (str): The tooltip text to be displayed when hovering over the icon button.
        on_click (function, optional): The callback function to be executed when the icon button is clicked. Default is None.

        Returns:
        None

        Note:
        The icon button's size is set to 512x512 pixels, its height is fixed to 40 pixels, and its width is fixed to 100 pixels.
        The separator line is a vertical line with a sunken frame shadow and a color of #afb2b7.
        """
        icon_size = QSize(512, 512)
        nonlocal buttons
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
        buttons.append(icon_button)

    add_icon_to_layout(grey_layout, 'assets/iconHomepage.png', text_translate[0], run_home_comeback)
    add_icon_to_layout(grey_layout, 'assets/iconRun.png', text_translate[1], run_search_callback)
    add_icon_to_layout(grey_layout, 'assets/iconSettings.png', text_translate[2], setting_window.show)
    add_icon_to_layout(grey_layout, 'assets/iconHelp.png', text_translate[3], help_window.show)
    add_icon_to_layout(grey_layout, 'assets/iconInformation.png', text_translate[4], about_window.show)
    grey_strip.setLayout(grey_layout)
    return white_strip, grey_strip, buttons



