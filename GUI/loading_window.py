from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt


class LoadingWindow(QDialog):
    """
    A class to create a loading window with a GIF animation.

    Attributes
    ----------
    parent : QWidget
        the parent widget of the dialog (default is None)

    Methods
    -------
    start_animation():
        starts the GIF animation
    stop_animation():
        stops the GIF animation
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Загрузка')
        self.setFixedSize(300, 300)
        self.setStyleSheet("background-color: #ffffff;")
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()

        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("assets/iconLoading.gif")
        self.gif_label.setMovie(self.movie)
        layout.addWidget(self.gif_label)

        self.setLayout(layout)
        self.start_animation()

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
