import math
from fractions import Fraction

class Calculator:
    def __init__(self):
        self.operators = {
            "+": {"arity": 2, "func": lambda a, b: a + b, "precedence": 1},
            "-": {"arity": 2, "func": lambda a, b: a - b, "precedence": 1},
            "*": {"arity": 2, "func": lambda a, b: a * b, "precedence": 2},
            "/": {"arity": 2, "func": lambda a, b: Fraction(a) / Fraction(b) if b != 0 else float('inf'), "precedence": 2},
            "^": {"arity": 2, "func": lambda a, b: a ** b, "precedence": 3},
            "sqrt": {"arity": 1, "func": lambda a: math.sqrt(a), "precedence": 4},
            "sin": {"arity": 1, "func": lambda a: math.sin(a), "precedence": 4},
            "cos": {"arity": 1, "func": lambda a: math.cos(a), "precedence": 4},
            "tan": {"arity": 1, "func": lambda a: math.tan(a), "precedence": 4},
            "log": {"arity": 1, "func": lambda a: math.log10(a), "precedence": 4},
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
                    # Convert to Fraction if possible, otherwise float
                    values.append(Fraction(token))
                except ValueError:
                    raise ValueError(f"Unknown token: '{token}'. Please check for typos or unsupported operations.")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            if len(values) > 1:
                raise ValueError("Expression is incomplete or has missing operators. Found extra numbers.")
            else:
                raise ValueError("Expression is malformed.")

        return values[0]

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
            except ValueError as e:
                raise ValueError(f"Mathematical error during operation '{operator}': {e}")
