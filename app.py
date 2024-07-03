import sys
from PyQt5.QtWidgets import QApplication
from GUI.main_window import MainWindow
from core.settings_handler import get_language
from database.db import create_database, delete_database
from logger import logger
from translations.translator import TranslatorManager


def main():
    logger.info("Start app")
    create_database()
    import multiprocessing
    multiprocessing.set_start_method('spawn')
    try:
        app = QApplication(sys.argv)
        translator_manager = TranslatorManager()
        current_language = get_language()
        if current_language:
            translator_manager.load_translation(current_language)
        translator_manager.install_translation(app)

        window = MainWindow(translator_manager=translator_manager, app=app)
        window.show()
        app.aboutToQuit.connect(lambda: delete_database())
        sys.exit(app.exec_())
    except Exception as e:
        logger.exception("Error while starting")
        sys.exit(1)


if __name__ == "__main__":
    main()
