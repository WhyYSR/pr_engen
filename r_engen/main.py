import flet as ft
from main_window import MainWindow


def main(page: ft.Page):
    """Это основная функция, которая запускает приложение.
    Она принимает один параметр: page (страница, на которой отображается приложение)."""
    interface = MainWindow(page)
    interface.main_window_page()


if __name__ == "__main__":
    ft.app(target=main)
