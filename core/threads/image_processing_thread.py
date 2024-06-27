from PyQt5.QtCore import QThread, pyqtSignal

from core.find_duplicate import get_results_find_duplicates


class ImageProcessingThread(QThread):
    results_ready = pyqtSignal(list)

    def __init__(self, image_paths_above, image_paths_below):
        super().__init__()
        self.image_paths_above = image_paths_above
        self.image_paths_below = image_paths_below

    def run(self):
        results = get_results_find_duplicates(self.image_paths_above, self.image_paths_below)
        self.results_ready.emit(results)
