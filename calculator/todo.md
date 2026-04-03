# TODO: Add Decimal to Fraction conversion

The user wants to use the calculator to convert decimals to fractions. Currently, the `Calculator` class evaluates expressions using complex numbers and floating-point math, and does not support automatic conversion to `fractions.Fraction`.

## Tasks
- [ ] Investigate `fractions.Fraction` module integration within `Calculator.evaluate`.
- [ ] Determine if a specific command or function (e.g., `frac(0.5)`) should be implemented for conversion.
- [ ] Update `main.py`'s `format_result` if necessary to ensure fractions are rendered correctly if the evaluation engine starts supporting them.
- [ ] Add unit tests for decimal-to-fraction conversion.
