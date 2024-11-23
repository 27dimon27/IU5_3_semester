import unittest

from RK2 import *

class TestBookshopAnalysis(unittest.TestCase):

    def setUp(self):
        """Инициализация данных для тестов"""
        self.books = [
            Book(1, "Python 101", 25.99, 1),
            Book(2, "Advanced Python", 35.50, 2),
            Book(3, "Learning AI", 40.00, 1),
        ]

        self.bookshops = [
            BookShop(1, "Tech Books"),
            BookShop(2, "Programming Hub")
        ]

        self.sales = [
            Sales(1, 1),
            Sales(2, 2),
            Sales(3, 1),
        ]

    def test_task_a1(self):
        """Тест для задачи A1"""
        one_to_many = create_one_to_many(self.books, self.bookshops)
        result = task_a1(one_to_many)
        expected = [
            ("Advanced Python", 35.50, "Programming Hub"),
            ("Python 101", 25.99, "Tech Books"),
            ("Learning AI", 40.00, "Tech Books")
        ]
        self.assertEqual(result, expected)


    def test_task_a2(self):
        """Тест для задачи A2"""
        one_to_many = create_one_to_many(self.books, self.bookshops)
        result = task_a2(one_to_many, self.bookshops)
        expected = [("Tech Books", 65.99), ("Programming Hub", 35.50)]
        self.assertEqual(result, expected)

    def test_task_a3(self):
        """Тест для задачи A3"""
        many_to_many = create_many_to_many(self.books, self.bookshops, self.sales)
        result = task_a3(many_to_many, self.bookshops)
        expected = {"Tech Books": ["Python 101", "Learning AI"]}
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()