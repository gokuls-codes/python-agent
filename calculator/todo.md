# Todo List for Fixing the Calculator

- [x] Analyze `pkg/calculator.py` to identify the issue with operator precedence.
- [x] Correct the `precedence` dictionary in `Calculator` class.
    - Currently `+` (4) > `*` (1) which is incorrect mathematically (Multiplication and Division should have higher precedence than Addition and Subtraction).
- [x] Run `tests.py` to verify the fixes and ensure no regressions.
