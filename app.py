import sys
from PyQt5.QtWidgets import QApplication
from GUI.main_window import MainWindow
from database.db import create_database, delete_database
from logger import logger


def main():
    logger.info("Start app")
    create_database()
    import multiprocessing
    multiprocessing.set_start_method('spawn')
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.aboutToQuit.connect(lambda: delete_database())
        sys.exit(app.exec_())
    except Exception as e:
        logger.exception("Error while starting")
        sys.exit(1)


if __name__ == "__main__":
    main()
