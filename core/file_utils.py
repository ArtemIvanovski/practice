import os

from core.settings_handler import read_settings_from_json


def get_files_in_folder(folder_path):
    format_settings = {
        "bmp": ".bmp",
        "png": ".png",
        "gif": ".gif",
        "jpeg": ".jpeg"
    }

    formats = [format for key, format in format_settings.items() if read_settings_from_json(key)]

    files_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(format) for format in formats):
                files_list.append(os.path.join(root, file))
    return files_list
