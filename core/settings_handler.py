from logger import logger
import json


def get_language():
    """
    This function reads the 'settings.json' file and determines the user's preferred language.

    Parameters:
    None

    Returns:
    str: The user's preferred language as a string. If the language is not found in the settings,
         it returns None.

    Raises:
    FileNotFoundError: If the 'settings.json' file is not found.
    json.JSONDecodeError: If there is a JSON decode error in the 'settings.json' file.
    Exception: For any other unexpected error.
    """
    try:
        with open("settings.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get("english"):
                return "english"
            elif data.get("russian"):
                return "russian"
            elif data.get("french"):
                return "french"
            elif data.get("belarusian"):
                return "belarusian"
    except FileNotFoundError as e:
        logger.error(f"File 'settings.json' not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in file 'settings.json': {e}")
    except Exception as e:
        logger.error(f"Error reading file 'settings.json': {e}")


def read_settings_from_json(field):
    """
    This function reads a specific field from the 'settings.json' file.

    Parameters:
    field (str): The name of the field to read from the JSON file.

    Returns:
    Any: The value of the specified field in the JSON file. If the field is not found,
         it returns None.

    Raises:
    FileNotFoundError: If the 'settings.json' file is not found.
    json.JSONDecodeError: If there is a JSON decode error in the 'settings.json' file.
    Exception: For any other unexpected error.
    """
    try:
        with open("settings.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(field)
    except FileNotFoundError as e:
        logger.error(f"File 'settings.json' not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in file 'settings.json': {e}")
    except Exception as e:
        logger.error(f"Error reading file 'settings.json': {e}")


def write_settings_to_json(settings):
    """
    This function writes the provided settings to the 'settings.json' file.

    Parameters:
    settings (dict): A dictionary containing the settings to be written to the JSON file.

    Returns:
    None

    Raises:
    Exception: If there is an error writing to the 'settings.json' file.

    Note:
    The function uses the 'json.dump' method with 'ensure_ascii=False' and 'indent=4' to ensure
    proper formatting of the JSON output.
    """
    try:
        with open("settings.json", 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        logger.info(f"Settings successfully written to 'settings.json'.")
    except Exception as e:
        logger.error(f"Error writing to file 'settings.json': {e}")
