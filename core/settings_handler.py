from logger import logger
import json


def read_settings_from_json(field):
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
    try:
        with open("settings.json", 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        logger.info(f"Settings successfully written to 'settings.json'.")
    except Exception as e:
        logger.error(f"Error writing to file 'settings.json': {e}")
