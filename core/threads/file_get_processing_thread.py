from PyQt5.QtCore import QThread, pyqtSignal

from core.file_utils import get_files_in_folder


class FileGetProcessingThread(QThread):
    """
    A QThread subclass that processes files in a given folder.
    Emits a signal 'finished' with a list of image paths and a list of error image paths.
    """

    # Signal definition: finished(list, list)
    finished = pyqtSignal(list, list)

    def __init__(self, folder_path):
        """
        Initialize the FileGetProcessingThread with the given folder path.

        :param folder_path: str, The path of the folder to process.
        """
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        """
        Run the file processing.

        Calls the get_files_in_folder function to get the image paths and error image paths.
        Emits the 'finished' signal with the obtained image paths and error image paths.
        """
        image_paths, error_image_path = get_files_in_folder(self.folder_path)
        self.finished.emit(image_paths, error_image_path)
