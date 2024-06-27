from PyQt5.QtCore import QThread, pyqtSignal

from GUI.similar_images_window import SimilarImagesWindow


class SimilarImagesProcessingThread(QThread):
    results_ready = pyqtSignal(list)

    def __init__(self, similar_images, width, height):
        super().__init__()
        self.similar_images = similar_images
        self.width = width
        self.height = height

    def run(self):
        similar_images_window = SimilarImagesWindow(self.similar_images, self.width, self.height)
        self.results_ready.emit(similar_images_window)
