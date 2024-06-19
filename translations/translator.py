from PyQt5.QtCore import QTranslator, QLocale


class TranslatorManager:
    def __init__(self):
        self.translator = QTranslator()

    def load_system_translation(self):
        system_locale = QLocale.system().name()
        self.load_translation(system_locale)

    def load_translation(self, language_code):
        self.translator.load(f'{language_code}.qm')

    def install_translation(self, app):
        app.installTranslator(self.translator)

    def remove_translation(self, app):
        app.removeTranslator(self.translator)
