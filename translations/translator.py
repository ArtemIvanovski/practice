from PyQt5.QtCore import QTranslator, QLocale

from logger import logger


class TranslatorManager:
    def __init__(self):
        self.translator = QTranslator()
        self.current_language = None

    def load_system_translation(self):
        system_locale = QLocale.system().name()
        self.load_translation(system_locale)

    def load_translation(self, language_code):
        self.current_language = language_code
        translation_file = f'translations/app_{language_code}.qm'
        if not self.translator.load(translation_file):
            logger.error(f"Translation file {translation_file} not found.")
        else:
            logger.info(f"Loaded translation file {translation_file}.")

    def install_translation(self, app):
        app.installTranslator(self.translator)

    def remove_translation(self, app):
        app.removeTranslator(self.translator)

    def change_language(self, app, language_code):
        self.remove_translation(app)
        self.load_translation(language_code)
        self.install_translation(app)
