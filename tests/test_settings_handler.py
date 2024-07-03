import json
from unittest import mock
from unittest.mock import mock_open, patch
from core.settings_handler import get_language, read_settings_from_json, get_finder_settings


def test_get_language():
    mock_data = {
        "english": True,
        "russian": False,
        "french": False,
        "belarusian": False
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        with patch("core.settings_handler.logger") as mock_logger:
            assert get_language() == "en"
            mock_logger.error.assert_not_called()

    mock_data = {
        "english": False,
        "russian": True,
        "french": False,
        "belarusian": False
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        assert get_language() == "ru"

    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("core.settings_handler.logger") as mock_logger:
            assert get_language() is None
            mock_logger.error.assert_called_once_with(mock.ANY)

    with patch("builtins.open", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
        with patch("core.settings_handler.logger") as mock_logger:
            assert get_language() is None
            mock_logger.error.assert_called_once_with(mock.ANY)


def test_read_settings_from_json():
    mock_data = {
        "similarity_threshold": 0.8,
        "aHash": True,
        "gHash": True,
        "pHash": True,
        "dHash": True
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        assert read_settings_from_json("similarity_threshold") == 0.8

    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("core.settings_handler.logger") as mock_logger:
            assert read_settings_from_json("nonexistent_field") is None
            mock_logger.error.assert_called_once_with(mock.ANY)

    with patch("builtins.open", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
        with patch("core.settings_handler.logger") as mock_logger:
            assert read_settings_from_json("similarity_threshold") is None
            mock_logger.error.assert_called_once_with(mock.ANY)


def test_get_finder_settings():
    mock_data = {
        "similarity_threshold": 0.8,
        "aHash": True,
        "gHash": True,
        "pHash": True,
        "dHash": True
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        assert get_finder_settings() == (0.8, True, True, True, True)

    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("core.settings_handler.logger") as mock_logger:
            assert get_finder_settings() == (None, None, None, None, None)
            mock_logger.error.assert_called()
