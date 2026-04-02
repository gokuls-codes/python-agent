# Plan to add division to the calculator

1. **Modify `pkg/calculator.py`**:
    - Add the division operator (`/`) to `self.operators` in the `Calculator.__init__` method.
    - Implement the division logic, ensuring to handle division by zero.
    - Update `self.precedence` to include `/` with the same precedence as multiplication (`*`).

2. **Verify changes**:
    - Run the calculator to ensure `/` is parsed and evaluated correctly.
    - Add a test case for division in `tests.py` if necessary.

3. **Final check**:
    - Ensure division by zero raises an appropriate error.
