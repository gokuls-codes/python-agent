import unittest
from pkg.calculator import Calculator
from fractions import Fraction

class TestFractionConversion(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_frac_function(self):
        # We want to support something like `frac 0.5`
        # Or even just automatic conversion if a user asks for it.
        # Let's start by adding a `frac` function to the calculator
        result = self.calc.evaluate("frac 0.5")
        self.assertEqual(result, Fraction(1, 2))

if __name__ == '__main__':
    unittest.main()
