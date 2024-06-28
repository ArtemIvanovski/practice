from PyQt5.QtCore import QThread, pyqtSignal

from GUI.image_viewer_window import ImageViewer


class ViewerProcessingThread(QThread):
    """
    A QThread subclass for processing images in a separate thread.
    Emits a signal when processing is finished, passing the ImageViewer instance.

    Attributes:
    finished : pyqtSignal(object)
        Signal emitted when processing is finished.
    """

    def __init__(self, image_paths):
        """
        Initialize the ViewerProcessingThread with a list of image paths.

        Parameters:
        image_paths (list): A list of paths to the images to be processed.
        """
        super().__init__()
        self.image_paths = image_paths

    def run(self):
        """
        Run the processing in a separate thread.
        Creates an ImageViewer instance with the given image paths and emits the finished signal.
        """
        viewer_window = ImageViewer(self.image_paths)
        self.finished.emit(viewer_window)
