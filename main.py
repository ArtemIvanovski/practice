import sys
from PyQt5.QtWidgets import QApplication
from GUI.main_window import MainWindow
from logger import logger


def main():
    logger.info("Start app")
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.exception("Error while starting")
        sys.exit(1)


if __name__ == "__main__":
    main()
