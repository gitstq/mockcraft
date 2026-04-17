"""
MockCraft - YAML-driven structured test data factory.
Zero-dependency Python implementation.
"""
__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .core import MockCraft
from .engine import DataEngine

__all__ = ["MockCraft", "DataEngine", "__version__"]
