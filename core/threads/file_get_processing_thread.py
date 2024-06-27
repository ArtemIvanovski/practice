from PyQt5.QtCore import QThread, pyqtSignal

from core.file_utils import get_files_in_folder


class FileGetProcessingThread(QThread):
    finished = pyqtSignal(list, list)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        image_paths, error_image_path = get_files_in_folder(self.folder_path)
        self.finished.emit(image_paths, error_image_path)
