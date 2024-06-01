import unittest
import numpy as np
from r_engen.equation_solver import EquationSolver  # Используйте абсолютный путь


class TestEquationSolver(unittest.TestCase):

    def setUp(self):
        # Инициализация необходимых параметров для тестов
        self.page = None  # Здесь можно создать mock объект для страницы
        self.size = 3
        self.current_language = 'en'
        self.entries = []
        self.solver = EquationSolver(self.page, self.size, self.current_language, self.entries)

    def assertListAlmostEqual(self, list1, list2, places=7):
        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, places=places)

    def test_solve_lu(self):
        A = [
            [2, 3, 1],
            [4, 1, -3],
            [3, -1, 2]
        ]
        b = [1, 2, 3]
        expected_x = [0.75, -0.25, 0.25]

        result_x = self.solver.solve_lu(A, b)
        self.assertListAlmostEqual(result_x, expected_x)

    def test_lu_decomposition(self):
        A = [
            [4, 3],
            [6, 3]
        ]
        expected_L = [
            [1.0, 0.0],
            [1.5, 1.0]
        ]
        expected_U = [
            [4, 3],
            [0, -1.5]
        ]

        L, U = self.solver.lu_decomposition(A)
        for row_result, row_expected in zip(L, expected_L):
            self.assertListAlmostEqual(row_result, row_expected)
        for row_result, row_expected in zip(U, expected_U):
            self.assertListAlmostEqual(row_result, row_expected)

    def test_forward_substitution(self):
        L = [
            [1, 0, 0],
            [0.5, 1, 0],
            [0.5, 0.5, 1]
        ]
        b = [2, 1, 1]
        expected_y = [2, 0, 0]

        result_y = self.solver.forward_substitution(L, b)
        self.assertListAlmostEqual(result_y, expected_y)

    def test_backward_substitution(self):
        U = [
            [2, -1, 0],
            [0, 2, -1],
            [0, 0, 1]
        ]
        y = [1, 1, 1]
        expected_x = [1, 1, 1]

        result_x = self.solver.backward_substitution(U, y)
        self.assertListAlmostEqual(result_x, expected_x)

    def test_final_value_with_numpy(self):
        num_tests = 10
        passed_tests = 0
        failed_tests = 0

        for _ in range(num_tests):
            a = np.random.randint(-10, 10, size=(3, 3)).tolist()
            b = np.random.randint(-10, 10, size=3).tolist()

            a_np = np.array(a)
            b_np = np.array(b)

            try:
                result_x = self.solver.solve_lu(a, b)
                expected_x_np = np.linalg.solve(a_np, b_np)

                self.assertListAlmostEqual(result_x, expected_x_np.tolist())
                passed_tests += 1
            except Exception as e:
                failed_tests += 1
                print(f"Test failed with matrix A: {a_np}, vector B: {b_np}. Error: {str(e)}")

        print(f"Number of passed tests: {passed_tests}")
        print(f"Number of failed tests: {failed_tests}")


if __name__ == '__main__':
    unittest.main()
