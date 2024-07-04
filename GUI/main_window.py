import time
from multiprocessing import Process, Queue
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QApplication
from PyQt5.QtGui import QIcon
from GUI.error_window import ErrorWindow
from GUI.image_viewer_window import run_image_viewer
from GUI.loading_window import LoadingWindow
from GUI.result_window import ResultsWindow
from GUI.top_bar_with_icons import create_top_bar_with_icons, create_button
from core.settings_handler import get_language
from core.threads.file_get_processing_thread import FileGetProcessingThread
from core.threads.image_processing_thread import ImageProcessingThread


class MainWindow(QMainWindow):
    def __init__(self, translator_manager, app):
        super().__init__()
        self.translator_manager = translator_manager
        self.app = app
        self.viewer_process = None
        self.image_processing_thread = None
        self.worker_thread = None
        self.loading_window = None
        self.folder_path_above = None
        self.folder_path_below = None
        self.image_paths_below = []
        self.image_paths_above = []

        self.setWindowTitle('Image Duplicate Finder')
        self.setStyleSheet("background-color: #f3f3f3;")
        self.setWindowIcon(QIcon('assets/icon.png'))

        screen_geometry = QApplication.desktop().screenGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        self.setFixedSize(self.screen_width, self.screen_height)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.viewer_window = None
        self.results_window = None

        white_strip, grey_strip, self.buttons, self.setting_window = create_top_bar_with_icons(self, self.run_search,
                                                                                               None,
                                                                                               translator_manager, app,
                                                                                               None)

        self.layout.addWidget(white_strip)
        self.layout.addWidget(grey_strip)
        self.layout.addWidget(white_strip)
        self.layout.addWidget(white_strip)
        self.layout.addWidget(white_strip)
        self.layout.addWidget(white_strip)

        button_layout_above = QHBoxLayout()

        self.add_folder_button_above = create_button(self.tr("Добавить папку с изображениями"),
                                                     "assets/iconAddFolder.png")
        self.add_folder_button_above.clicked.connect(self.select_folder_above)
        button_layout_above.addWidget(self.add_folder_button_above)

        self.view_images_button_above = create_button(self.tr("Просмотреть изображения в папке"), "assets/iconView.png")
        self.view_images_button_above.clicked.connect(lambda: self.view_images_in_folder(False))
        button_layout_above.addWidget(self.view_images_button_above)

        self.layout.addLayout(button_layout_above)

        button_layout_below = QHBoxLayout()

        self.add_folder_button_below = create_button(self.tr("Добавить папку с изображениями"),
                                                     "assets/iconAddFolder.png")
        self.add_folder_button_below.clicked.connect(self.select_folder_below)
        button_layout_below.addWidget(self.add_folder_button_below)

        self.view_images_button_below = create_button(self.tr("Просмотреть изображения в папке"), "assets/iconView.png")
        self.view_images_button_below.clicked.connect(lambda: self.view_images_in_folder(True))
        button_layout_below.addWidget(self.view_images_button_below)

        self.layout.addLayout(button_layout_below)

        content_strip = QWidget()
        self.layout.addWidget(content_strip)

        self.main_widget.setLayout(self.layout)

    def select_folder_above(self):
        self.folder_path_above = QFileDialog.getExistingDirectory(self, self.tr('Выбрать папку'))
        if self.folder_path_above:
            self.start_loading(self.folder_path_above, self.on_folder_above_loaded)
        else:
            self.image_paths_above = []
            self.add_folder_button_above.setText(self.tr("Добавить папку с изображениями"))
            self.add_folder_button_above.setIcon(QIcon("assets/iconAddFolder.png"))

    def select_folder_below(self):
        self.folder_path_below = QFileDialog.getExistingDirectory(self, self.tr('Выбрать папку'))
        if self.folder_path_below:

            self.start_loading(self.folder_path_below, self.on_folder_below_loaded)
        else:
            self.image_paths_below = []
            self.add_folder_button_below.setText(self.tr("Добавить папку с изображениями"))
            self.add_folder_button_below.setIcon(QIcon("assets/iconAddFolder.png"))

    def start_loading(self, folder_path, callback):
        self.loading_window = LoadingWindow(self)
        self.loading_window.show()

        self.worker_thread = FileGetProcessingThread(folder_path)
        self.worker_thread.finished.connect(callback)
        self.worker_thread.start()

    def on_folder_above_loaded(self, image_paths, error_image_path):
        tr_msg = self.tr("Выбранная папка: ")
        self.add_folder_button_above.setText(tr_msg + self.folder_path_above.split('/')[-1])
        self.add_folder_button_above.setIcon(QIcon("assets/iconRemoveFolder.png"))
        self.loading_window.close()
        self.image_paths_above = image_paths
        if len(error_image_path) > 0:
            error_image_path_string = '\n'.join(path for path in error_image_path)
            tr_msg = self.tr("Данные изображения повреждены:")
            error_dialog = ErrorWindow(tr_msg + "\n" + error_image_path_string)
            error_dialog.exec_()
        if len(self.image_paths_above) == 0:
            error_dialog = ErrorWindow(self.tr("В данной папке нет изображений выбранного формата"))
            error_dialog.exec_()
            self.folder_path_above = None
            self.add_folder_button_above.setText(self.tr("Добавить папку с изображениями"))
            self.add_folder_button_above.setIcon(QIcon("assets/iconAddFolder.png"))

    def on_folder_below_loaded(self, image_paths, error_image_path):
        tr_msg = self.tr("Выбранная папка: ")
        self.add_folder_button_below.setText(tr_msg + self.folder_path_below.split('/')[-1])
        self.add_folder_button_below.setIcon(QIcon("assets/iconRemoveFolder.png"))
        self.loading_window.close()
        self.image_paths_below = image_paths
        if len(error_image_path) > 0:
            error_image_path_string = '\n'.join(path for path in error_image_path)
            tr_msg = self.tr("Данные изображения повреждены: ")
            error_dialog = ErrorWindow(tr_msg + "\n" + error_image_path_string)
            error_dialog.exec_()
        if len(self.image_paths_below) == 0:
            error_dialog = ErrorWindow(self.tr("В данной папке нет изображений выбранного формата"))
            error_dialog.exec_()
            self.folder_path_below = None
            self.add_folder_button_below.setText(self.tr("Добавить папку с изображениями"))
            self.add_folder_button_below.setIcon(QIcon("assets/iconAddFolder.png"))

    def view_images_in_folder(self, is_below_folder):
        if is_below_folder:
            if self.folder_path_below is not None and self.folder_path_below != "":
                image_paths = self.image_paths_below
            else:
                error_dialog = ErrorWindow(self.tr("Папка ниже не выбрана"))
                error_dialog.exec_()
                return
        else:
            if self.folder_path_above is not None and self.folder_path_above != "":
                image_paths = self.image_paths_above
            else:
                error_dialog = ErrorWindow(self.tr("Папка сверху не выбрана"))
                error_dialog.exec_()
                return
        if not image_paths:
            error_dialog = ErrorWindow(self.tr("Нет изображений выбранного типа"))
            error_dialog.exec_()
            return

        self.start_viewer_loading(image_paths)

    def start_viewer_loading(self, image_paths):
        self.loading_window = LoadingWindow(self)
        self.loading_window.show()
        queue = Queue()

        self.viewer_process = Process(target=run_image_viewer, args=(image_paths, queue))
        self.viewer_process.start()

        while True:
            if not queue.empty():
                message = queue.get()
                if message == 'done':
                    self.loading_window.close()
                    break
            time.sleep(0.1)

    def run_search(self):
        if not self.image_paths_above and not self.image_paths_below:
            error_dialog = ErrorWindow(self.tr("Выберите папку с изображениями"))
            error_dialog.exec_()
            return

        self.loading_window = LoadingWindow(self)
        self.loading_window.show()

        self.image_processing_thread = ImageProcessingThread(
            self.image_paths_above, self.image_paths_below,
        )
        self.image_processing_thread.results_ready.connect(self.on_results_ready)
        self.image_processing_thread.start()

    def on_results_ready(self, results):
        self.loading_window.close()
        self.results_window = ResultsWindow(self, results, self.translator_manager, self.app)
        self.results_window.show()
        self.setHidden(True)

    def showEvent(self, event):
        self.showMaximized()
        self.setFixedSize(self.screen_width, self.screen_height)
        super().showEvent(event)

    def update_ui_texts(self):
        if len(self.image_paths_above) != 0:
            tr_msg = self.tr("Выбранная папка: ")
            self.add_folder_button_above.setText(tr_msg + self.folder_path_above.split('/')[-1])
        else:
            self.add_folder_button_above.setText(self.tr("Добавить папку с изображениями"))

        if len(self.image_paths_below) != 0:
            tr_msg = self.tr("Выбранная папка: ")
            self.add_folder_button_below.setText(tr_msg + self.folder_path_below.split('/')[-1])
        else:
            self.add_folder_button_below.setText(self.tr("Добавить папку с изображениями"))
        self.view_images_button_above.setText(self.tr("Просмотреть изображения в папке"))
        self.view_images_button_below.setText(self.tr("Просмотреть изображения в папке"))

        text_translate = ['Хочу домой', 'Запустить поиск', 'Настройки', 'Мне нужна помощь', 'Информация о приложении']

        code_language = get_language()

        if code_language == 'en':
            text_translate = ['Go home', 'Start the search', 'Settings', 'I need help',
                              'Information about the application']
        elif code_language == 'be':
            text_translate = ['Жадаю дадому', 'Запусціць пошук', 'Налады', 'Мне патрэбна дапамога',
                              'Інфармацыя аб праграме']
        elif code_language == 'fr':
            text_translate = ['Je veux rentrer à la maison', 'Lancer la recherche', 'Réglages', 'Jai besoin daide',
                              'Informations sur lapplication']

        for i, button in enumerate(self.buttons):
            button.setToolTip(text_translate[i])
