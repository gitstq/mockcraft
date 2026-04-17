"""
MockCraft Number Provider - integers, floats, ranges.
"""
import random
import math


class NumberProvider:
    """Generates numeric values."""

    def generate(self, min: int = 0, max: int = 100, step: int = 1, **kwargs) -> int:
        """
        Generate an integer.

        Args:
            min: Minimum value (inclusive)
            max: Maximum value (inclusive)
            step: Step size
        """
        lo, hi = int(min), int(max)
        if lo > hi:
            lo, hi = hi, lo
        val = random.randint(lo, hi)
        if step > 1:
            val = lo + ((val - lo) // step) * step
        return val

    def float_generate(self, min: float = 0.0, max: float = 1.0, decimals: int = 2, **kwargs) -> float:
        """Generate a float."""
        lo, hi = float(min), float(max)
        if lo > hi:
            lo, hi = hi, lo
        val = random.uniform(lo, hi)
        return round(val, int(decimals))

    def int_generate(self, min: int = 0, max: int = 100, **kwargs) -> int:
        return self.generate(min, max, **kwargs)
