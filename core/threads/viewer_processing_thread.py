from PyQt5.QtCore import QThread, pyqtSignal

from GUI.image_viewer_window import ImageViewer


class ViewerProcessingThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths

    def run(self):
        viewer_window = ImageViewer(self.image_paths)
        self.finished.emit(viewer_window)
