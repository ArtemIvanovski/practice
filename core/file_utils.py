import os

from core.image_utils import is_valid_image
from core.settings_handler import read_settings_from_json


def get_files_in_folder(folder_path):
    """
    This function retrieves all valid image files from a given folder.

    Parameters:
    folder_path (str): The path of the folder to search for image files.

    Returns:
    tuple: A tuple containing two lists. The first list contains the paths of valid image files,
        and the second list contains the names of invalid image files.

    Raises:
    FileNotFoundError: If the specified folder does not exist.
    """
    format_settings = {
        "bmp": ".bmp",
        "png": ".png",
        "gif": ".gif",
        "jpeg": ".jpeg"
    }

    error_image = []

    formats = [format for key, format in format_settings.items() if read_settings_from_json(key)]

    files_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(format) for format in formats):
                if is_valid_image(os.path.join(root, file)):
                    files_list.append(os.path.join(root, file))
                else:
                    error_image.append(file)

    return files_list, error_image
