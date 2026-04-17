"""
MockCraft Core - YAML configuration parser and main orchestrator.
"""
import os
import sys
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from .engine import DataEngine
from .providers.registry import ProviderRegistry


class MockCraft:
    """
    Main entry point for MockCraft data generation.

    Load a YAML schema and generate structured fake data records
    with full customization control.
    """

    def __init__(self, locale: str = "zh_CN"):
        self.locale = locale
        self.registry = ProviderRegistry(locale)
        self.engine = DataEngine(self.registry)

    def load_yaml(self, yaml_path: Union[str, Path]) -> Dict[str, Any]:
        """Load and parse a YAML schema file."""
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"YAML schema not found: {yaml_path}")
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    def load_yaml_string(self, yaml_string: str) -> Dict[str, Any]:
        """Parse YAML from a string."""
        return yaml.safe_load(yaml_string)

    def generate(
        self,
        schema: Union[str, Path, Dict[str, Any]],
        count: int = 1,
        start_index: int = 1,
        seed: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate `count` records from a schema.

        Args:
            schema: YAML file path, or a dict/parsed YAML object.
            count: Number of records to generate.
            start_index: Starting index for indexed fields.
            seed: Random seed for reproducibility.

        Returns:
            List of generated records.
        """
        if seed is not None:
            self.engine.set_seed(seed)

        if isinstance(schema, (str, Path)):
            schema = self.load_yaml(schema)

        records = []
        for i in range(count):
            record = self.engine.generate_record(
                schema, index=start_index + i
            )
            records.append(record)

        return records

    def generate_stream(
        self,
        schema: Union[str, Path, Dict[str, Any]],
        count: int = 1,
        seed: Optional[int] = None,
    ):
        """
        Generator version of generate() — yields records one by one.
        Memory-efficient for large datasets.
        """
        if seed is not None:
            self.engine.set_seed(seed)

        if isinstance(schema, (str, Path)):
            schema = self.load_yaml(schema)

        for i in range(count):
            yield self.engine.generate_record(schema, index=i + 1)

    def print_record(self, record: Dict[str, Any], format: str = "table"):
        """Pretty-print a single record."""
        from .formatters import get_formatter
        formatter = get_formatter(format)
        print(formatter.format_record(record))

    def export(
        self,
        records: List[Dict[str, Any]],
        output_path: str,
        format: str = "json",
        **kwargs
    ):
        """Export records to a file."""
        from .formatters import get_formatter
        formatter = get_formatter(format)
        content = formatter.format_batch(records, **kwargs)
        Path(output_path).write_text(content, encoding="utf-8")

    def cli(self, args: Optional[List[str]] = None):
        """Launch the CLI interface."""
        from .cli.main import main
        return main(args)
