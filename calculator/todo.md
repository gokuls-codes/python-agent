# Task: Display division results as fractions

## Background
The current calculator implementation in `pkg/calculator.py` uses floating-point division for the `/` operator. The user wants the output to be displayed as a fraction when applicable.

## Current State
- `Calculator.evaluate` uses floating-point math.
- `main.py` formats the result, handling integer conversion for floats like `5.0`.

## Plan
1.  **Modify `pkg/calculator.py`**:
    - Update the division logic to use Python's `fractions.Fraction` module.
    - Handle division so that the result maintains fractional representation when it's not a whole number.
2.  **Modify `main.py`**:
    - Update the output formatting logic to correctly display `fractions.Fraction` objects.
3.  **Testing**:
    - Ensure basic arithmetic still works.
    - Add/Update tests to verify that `1 / 2` outputs `1/2` instead of `0.5`.

## Notes
- Need to import `fractions.Fraction`.
- Consider if all calculations should use `Fraction` or just the final output formatting. Using `Fraction` for the calculation chain might be cleaner to avoid precision issues.
