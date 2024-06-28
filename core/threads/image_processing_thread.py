from PyQt5.QtCore import QThread, pyqtSignal

from core.find_duplicate import get_results_find_duplicates


class ImageProcessingThread(QThread):
    """
    A QThread subclass for processing images in a separate thread.
    Emits a signal when the processing is complete.
    """

    # Signal to notify when the results are ready
    results_ready = pyqtSignal(list)

    def __init__(self, image_paths_above, image_paths_below):
        """
        Initialize the ImageProcessingThread with the paths of images to process.

        Parameters:
        image_paths_above (list): A list of paths to images in the upper directory.
        image_paths_below (list): A list of paths to images in the lower directory.
        """
        super().__init__()
        self.image_paths_above = image_paths_above
        self.image_paths_below = image_paths_below

    def run(self):
        """
        Run the image processing in a separate thread.
        Calls the get_results_find_duplicates function from the core.find_duplicate module
        and emits the results_ready signal with the results.
        """
        results = get_results_find_duplicates(self.image_paths_above, self.image_paths_below)
        self.results_ready.emit(results)
