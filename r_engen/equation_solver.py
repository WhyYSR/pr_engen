import flet as ft
class EquationSolver:
    """
    Класс для решения системы уравнений.

    Атрибуты:
    - page: объект страницы, на которой отображается решение.
    - size: размерность системы уравнений.
    - current_language: текущий язык интерфейса.
    - entries: введенные пользователем значения.
    """
    def __init__(self, page, size, current_language, entries):
        self.page = page
        self.size = size
        self.current_language = current_language
        self.entries = entries

    def the_triangular_matrix(self, A, B):
        """
        Приводит матрицу к треугольному виду.

        Параметры:
        - A: двумерный список (матрица коэффициентов системы уравнений)
        - B: список (столбец свободных членов)
        - page: объект страницы для отображения сообщений об ошибках

        Возвращает:
        - A: список (Матрица перемех) или None, если матрица не квадратная
        - B: список (решение системы уравнений)
        """
        n = len(A)
        if len(A) != len(A[0]):
            self.show_error_alert(self.page.translations['messages']['non_square_matrix_gauss'][self.current_language])
            return None, None

        det = 1
        epsilon = 1e-10

        for i in range(n):
            max_elem = abs(A[i][i])
            max_row = i

            # Поиск максимального элемента в текущем столбце
            for k in range(i + 1, n):
                if abs(A[k][i]) > max_elem:
                    max_elem = abs(A[k][i])
                    max_row = k

            # Обмен строк для улучшения численной устойчивости
            A[i], A[max_row] = A[max_row], A[i]
            B[i], B[max_row] = B[max_row], B[i]

            # Приведение матрицы к треугольному виду
            for j in range(i + 1, n):
                coef = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= coef * A[i][k]
                B[j] -= coef * B[i]

            # Расчет определителя
            det *= A[i][i]  # знак не важен

        A_test = [row for row in A if any(abs(el) > epsilon for el in row)]
        if len(A) != len(A_test):
            self.show_error_alert(self.page.translations['messages']['non_square_matrix_gauss'][self.current_language])
            return None, None

        return A, B

    def solve_lu(self, A, b):
        """
        Решает систему линейных уравнений методом LU-разложения.

        Параметры:
        - A: двумерный список (матрица коэффициентов системы уравнений)
        - b: список (столбец свободных членов)

        Возвращает:
        - x: список (решение системы уравнений)
        """
        L, U = self.lu_decomposition(A)
        y = self.forward_substitution(L, b)
        x = self.backward_substitution(U, y)
        return x

    def lu_decomposition(self, A):
        """
        Выполняет LU-разложение матрицы A.

        Параметры:
        - A: двумерный список (исходная матрица)

        Возвращает:
        - L: двумерный список (нижнетреугольная матрица L)
        - U: двумерный список (верхнетреугольная матрица U)
        """
        n = len(A)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]

        for i in range(n):
            L[i][i] = 1.0

        for k in range(n):
            U[k][k] = A[k][k]
            for j in range(k + 1, n):
                L[j][k] = A[j][k] / U[k][k]
                U[k][j] = A[k][j]
            for i in range(k + 1, n):
                for j in range(k + 1, n):
                    A[i][j] -= L[i][k] * U[k][j]

        return L, U

    def forward_substitution(self, L, b):
        """
        Выполняет прямую подстановку.

        Параметры:
        - L: двумерный список (нижнетреугольная матрица L)
        - b: список (столбец свободных членов)

        Возвращает:
        - y: список (результат прямой подстановки)
        """
        n = len(L)
        y = [0.0] * n
        for i in range(n):
            y[i] = b[i]
            for j in range(i):
                y[i] -= L[i][j] * y[j]
        return y

    def backward_substitution(self, U, y):
        """
        Выполняет обратную подстановку.

        Параметры:
        - U: двумерный список (верхнетреугольная матрица U)
        - y: список (результат прямой подстановки)

        Возвращает:
        - x: список (решение системы уравнений)
        """
        n = len(U)
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, n):
                x[i] -= U[i][j] * x[j]
            x[i] /= U[i][i]
        return x

    def show_error_alert(self, message):
        alert_dialog = self.page.dialog
        alert_dialog.title = ft.Text(self.page.translations['messages']['error'][self.current_language])
        alert_dialog.content = ft.Text(message)
        alert_dialog.actions = [ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        alert_dialog.actions_alignment = ft.MainAxisAlignment.END

        alert_dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()
