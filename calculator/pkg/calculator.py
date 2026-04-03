import math
import cmath
from fractions import Fraction

def solve_quadratic(a, b, c):
    """
    Solves ax^2 + bx + c = 0
    Returns a tuple of two roots.
    """
    if a == 0:
        if b == 0:
            raise ValueError("Not a quadratic equation (a=0 and b=0).")
        return (-c / b,)
    
    d = (b**2) - (4*a*c)
    
    root1 = (-b - cmath.sqrt(d)) / (2*a)
    root2 = (-b + cmath.sqrt(d)) / (2*a)
    
    return root1, root2

class Calculator:
    def __init__(self):
        self.operators = {
            "+": {"arity": 2, "func": lambda a, b: a + b, "precedence": 1},
            "-": {"arity": 2, "func": lambda a, b: a - b, "precedence": 1},
            "*": {"arity": 2, "func": lambda a, b: a * b, "precedence": 2},
            "/": {"arity": 2, "func": lambda a, b: (complex(a) / complex(b)) if b != 0 else float('inf'), "precedence": 2},
            "^": {"arity": 2, "func": lambda a, b: complex(a) ** complex(b), "precedence": 3},
            "sqrt": {"arity": 1, "func": lambda a: cmath.sqrt(complex(a)), "precedence": 4},
            "sin": {"arity": 1, "func": lambda a: cmath.sin(complex(a)), "precedence": 4},
            "cos": {"arity": 1, "func": lambda a: cmath.cos(complex(a)), "precedence": 4},
            "tan": {"arity": 1, "func": lambda a: cmath.tan(complex(a)), "precedence": 4},
            "log": {"arity": 1, "func": lambda a: cmath.log10(complex(a)), "precedence": 4},
            "frac": {"arity": 1, "func": lambda a: Fraction(str(a)).limit_denominator(), "precedence": 4},
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                op_info = self.operators[token]
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.operators[operators[-1]]["precedence"] >= op_info["precedence"]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    # Attempt to parse as complex directly
                    if 'j' in token or 'J' in token:
                        values.append(complex(token))
                    else:
                        # Try to parse as a float/int first, fallback to complex
                        try:
                            values.append(float(token))
                        except ValueError:
                            values.append(complex(token))
                except ValueError:
                    raise ValueError(f"Unknown token: '{token}'. Please check for typos or unsupported operations.")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            if len(values) > 1:
                raise ValueError("Expression is incomplete or has missing operators. Found extra numbers.")
            else:
                raise ValueError("Expression is malformed.")

        # Cleanup: convert complex numbers with 0 imaginary part to real/int
        res = values[0]
        if isinstance(res, complex) and abs(res.imag) < 1e-10:
            return res.real
        return res

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        op_info = self.operators[operator]
        
        if op_info["arity"] == 2:
            if len(values) < 2:
                raise ValueError(f"Operator '{operator}' requires 2 arguments, but found fewer.")
            b = values.pop()
            a = values.pop()
            
            if operator == "/" and b == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
                
            values.append(op_info["func"](a, b))
        elif op_info["arity"] == 1:
            if len(values) < 1:
                raise ValueError(f"Operator '{operator}' requires 1 argument, but found none.")
            a = values.pop()
            try:
                values.append(op_info["func"](a))
            except Exception as e:
                raise ValueError(f"Mathematical error during operation '{operator}': {e}")
