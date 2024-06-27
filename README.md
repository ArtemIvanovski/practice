# Нахождение дубликатов изображений

Это десктопное приложение на Python, предназначенное для нахождения дубликатов изображений. Приложение позволяет находить похожие изображения как в одной папке, так и между двумя различными папками. Оно предоставляет различные настройки, такие как выбор метода хэширования, процент схожести изображений, мультиязычность и другие. Приложение поддерживает различные форматы файлов: BMP, JPEG, PNG, GIF.

![В разработке](https://img.shields.io/badge/status-в%20разработке-yellow)
![Просмотры](https://visitor-badge.glitch.me/badge?page_id=ArtemIvanovski.practice&left_color=green&right_color=red)

## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-ci/cd)
- [Contributing](#contributing)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии
- [PyQt](https://riverbankcomputing.com/software/pyqt/intro)
- [SQLite](https://www.sqlite.org/index.html)
- [cv2 (OpenCV)](https://opencv.org/)
- [numpy](https://numpy.org/)
- [PIL (Pillow)](https://python-pillow.org/)

## Использование
Для установки и использования приложения, выполните следующие шаги:

Установите необходимые зависимости с помощью команды:
```sh
$ pip install -r requirements.txt 
```
Запустите приложение:
```sh
$ python app.py
```