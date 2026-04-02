# calculator/tests.py

import unittest
import math
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_exponentiation(self):
        result = self.calculator.evaluate("2 ^ 3")
        self.assertEqual(result, 8)

    def test_exponentiation_precedence(self):
        # 2 + 3 * 2 ^ 2 = 2 + 3 * 4 = 14
        result = self.calculator.evaluate("2 + 3 * 2 ^ 2")
        self.assertEqual(result, 14.0)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.evaluate("10 / 0")

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_bug_report(self):
        result = self.calculator.evaluate("3 + 7 * 2")
        self.assertEqual(result, 17)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_sqrt(self):
        result = self.calculator.evaluate("sqrt 16")
        self.assertEqual(result, 4.0)

    def test_sqrt_complex(self):
        # 2 + sqrt 9 = 2 + 3 = 5
        result = self.calculator.evaluate("2 + sqrt 9")
        self.assertEqual(result, 5.0)

    def test_sqrt_precedence(self):
        # sqrt 9 * 2 = 3 * 2 = 6
        result = self.calculator.evaluate("sqrt 9 * 2")
        self.assertEqual(result, 6.0)

    def test_not_enough_operands_sqrt(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("sqrt")

    def test_sin(self):
        result = self.calculator.evaluate("sin 0")
        self.assertEqual(result, math.sin(0))

    def test_cos(self):
        result = self.calculator.evaluate("cos 0")
        self.assertEqual(result, math.cos(0))

    def test_tan(self):
        result = self.calculator.evaluate("tan 0")
        self.assertEqual(result, math.tan(0))

    def test_log(self):
        result = self.calculator.evaluate("log 10")
        self.assertEqual(result, 1.0)

if __name__ == "__main__":
    unittest.main()
