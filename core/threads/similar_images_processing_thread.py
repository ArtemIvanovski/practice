from PyQt5.QtCore import QThread, pyqtSignal

from GUI.similar_images_window import SimilarImagesWindow


class SimilarImagesProcessingThread(QThread):
    """
    A QThread subclass for processing similar images. Emits a signal when processing is finished.
    """

    finished = pyqtSignal(object)

    def __init__(self, similar_images, width, height):
        """
        Initialize the SimilarImagesProcessingThread.

        Parameters:
        similar_images (list): A list of similar images.
        width (int): The width of the images.
        height (int): The height of the images.
        """
        super().__init__()
        self.similar_images = similar_images
        self.width = width
        self.height = height

    def run(self):
        """
        Run the processing of similar images.

        Emits the finished signal with an instance of SimilarImagesWindow.
        """
        similar_images_window = SimilarImagesWindow(self.similar_images, self.width, self.height)
        self.finished.emit(similar_images_window)
