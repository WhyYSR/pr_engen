import json

class LoadFiles:
    """
    Класс для загрузки файлов.

    Методы:
    - load_translations: загружает переводы из файла JSON.
    """
    def __init__(self):
        pass

    def load_translations(self, file_path):
        """
        Загружает переводы из файла JSON.

        Параметры:
        - file_path: str, путь к файлу с переводами.

        Возвращает:
        - dict, словарь с переводами.
        """
        translations = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                translations = json.load(file)
        except FileNotFoundError:
            print(f"Файл с переводами не найден: {file_path}")
        except json.JSONDecodeError:
            print(f"Ошибка декодирования файла с переводами: {file_path}")

        return translations
