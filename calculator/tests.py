import unittest
import math
import cmath
from fractions import Fraction
from pkg.calculator import Calculator, solve_quadratic

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
        result = self.calculator.evaluate("1 / 2")
        self.assertEqual(result, 0.5)

    def test_division_whole(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_exponentiation(self):
        result = self.calculator.evaluate("2 ^ 3")
        self.assertEqual(result, 8)

    def test_exponentiation_precedence(self):
        result = self.calculator.evaluate("2 + 3 * 2 ^ 2")
        self.assertEqual(result, 14)

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
        result = self.calculator.evaluate("2 + sqrt 9")
        self.assertEqual(result, 5.0)

    def test_sqrt_precedence(self):
        result = self.calculator.evaluate("sqrt 9 * 2")
        self.assertEqual(result, 6.0)

    def test_not_enough_operands_sqrt(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("sqrt")

    def test_sin(self):
        result = self.calculator.evaluate("sin 0")
        self.assertAlmostEqual(result, math.sin(0))

    def test_cos(self):
        result = self.calculator.evaluate("cos 0")
        self.assertAlmostEqual(result, math.cos(0))

    def test_tan(self):
        result = self.calculator.evaluate("tan 0")
        self.assertAlmostEqual(result, math.tan(0))

    def test_log(self):
        result = self.calculator.evaluate("log 10")
        self.assertEqual(result, 1.0)
    
    def test_complex_arithmetic(self):
        # (1 + 2j) + (3 + 4j) = 4 + 6j
        result = self.calculator.evaluate("1+2j + 3+4j")
        self.assertEqual(result, 4+6j)
        
        # (1 + 1j) * (1 - 1j) = 2
        result = self.calculator.evaluate("1+1j * 1-1j")
        self.assertEqual(result, 2+0j)
        
        # sqrt(-1) = 1j
        result = self.calculator.evaluate("sqrt -1")
        self.assertEqual(result, 1j)

class TestQuadratic(unittest.TestCase):
    def test_two_real_roots(self):
        # x^2 - 3x + 2 = 0 -> (x-1)(x-2) = 0 -> roots 1, 2
        roots = solve_quadratic(1, -3, 2)
        self.assertIn(1.0 + 0j, roots)
        self.assertIn(2.0 + 0j, roots)

    def test_one_real_root(self):
        # x^2 - 2x + 1 = 0 -> (x-1)^2 = 0 -> root 1
        roots = solve_quadratic(1, -2, 1)
        self.assertEqual(roots, (1.0 + 0j, 1.0 + 0j))

    def test_complex_roots(self):
        # x^2 + 1 = 0 -> roots i, -i
        roots = solve_quadratic(1, 0, 1)
        self.assertIn(0 + 1j, roots)
        self.assertIn(0 - 1j, roots)

    def test_invalid_quadratic(self):
        with self.assertRaises(ValueError):
            solve_quadratic(0, 0, 5)

if __name__ == "__main__":
    unittest.main()
