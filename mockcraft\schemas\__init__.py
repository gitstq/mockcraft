"""
MockCraft Schema Examples & Utilities.
"""
from pathlib import Path
from typing import Dict, Any

EXAMPLES_DIR = Path(__file__).parent.parent.parent / "examples"


def get_example(name: str) -> Dict[str, Any]:
    """Load an example schema by name."""
    path = EXAMPLES_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Example schema not found: {name}")
    import yaml
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_examples() -> list:
    """List all available example schemas."""
    return [p.stem for p in EXAMPLES_DIR.glob("*.yaml")]
