"""
MockCraft Data Generation Engine.
Processes field definitions and generates values via providers.
"""
import random
import re
import string
import hashlib
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


class DataEngine:
    """Core engine that interprets field schemas and generates values."""

    def __init__(self, registry):
        self.registry = registry
        self._seed_state = None

    def set_seed(self, seed: int):
        """Set random seed for reproducibility."""
        self._seed_state = seed
        random.seed(seed)

    def _resolve_field(self, field_name: str, field_def: Any) -> Any:
        """Resolve a single field from its definition."""
        if isinstance(field_def, str):
            return self._resolve_string_field(field_def)
        elif isinstance(field_def, dict):
            return self._resolve_dict_field(field_def)
        elif isinstance(field_def, list):
            return self._resolve_list_field(field_def)
        else:
            return field_def

    def _resolve_string_field(self, value: str) -> str:
        """Handle string field definitions with {{}} expressions."""
        if "{{" not in value or "}}" not in value:
            return value

        result = value
        # Process {{index}} - already handled at record level
        # Process {{random.int min max}} or {{random.float min max}}
        float_pattern = r'\{\{random\.float\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*(?:,\s*(\d+))?\}\}'
        for match in re.finditer(float_pattern, result):
            lo, hi = float(match.group(1)), float(match.group(2))
            decimals = int(match.group(3)) if match.group(3) else 2
            val = round(random.uniform(lo, hi), decimals)
            result = result[:match.start()] + str(val) + result[match.end():]

        int_pattern = r'\{\{random\.int\s+(-?\d+)\s+(-?\d+)\}\}'
        for match in re.finditer(int_pattern, result):
            lo, hi = int(match.group(1)), int(match.group(2))
            result = result[:match.start()] + str(random.randint(lo, hi)) + result[match.end():]

        # Process {{random.choice a,b,c}} or {{random.choice [a,b,c]}}
        choice_pattern = r'\{\{random\.choice\s+(.+?)\}\}'
        for match in re.finditer(choice_pattern, result):
            choices_str = match.group(1).strip()
            if ',' in choices_str and not choices_str.startswith('['):
                choices = [c.strip() for c in choices_str.split(',')]
            else:
                try:
                    choices = eval(choices_str)
                    if isinstance(choices, list):
                        choices = choices
                    else:
                        choices = [choices_str]
                except Exception:
                    choices = [choices_str]
            val = random.choice(choices)
            result = result[:match.start()] + str(val) + result[match.end():]

        # Process {{random.uuid}}
        uuid_pattern = r'\{\{random\.uuid\}\}'
        for match in re.finditer(uuid_pattern, result):
            import uuid
            val = str(uuid.uuid4())
            result = result[:match.start()] + val + result[match.end():]

        # Process {{random.bool}}
        bool_pattern = r'\{\{random\.bool\}\}'
        for match in re.finditer(bool_pattern, result):
            val = str(random.choice([True, False])).lower()
            result = result[:match.start()] + val + result[match.end():]

        # Process {{timestamp}} or {{timestamp format=...}}
        ts_pattern = r'\{\{timestamp(?:\s+format=["\'](.+?)["\'])?\}\}'
        for match in re.finditer(ts_pattern, result):
            fmt = match.group(1) if match.group(1) else "%Y-%m-%dT%H:%M:%S"
            val = datetime.now().strftime(fmt)
            result = result[:match.start()] + val + result[match.end():]

        # Process {{date offset=... format=...}}
        date_pattern = r'\{\{date(?:\s+offset=["\'](.+?)["\'])?(?:\s+format=["\'](.+?)["\'])?\}\}'
        for match in re.finditer(date_pattern, result):
            offset_str = match.group(1) or "0"
            fmt = match.group(2) or "%Y-%m-%d"
            try:
                offset_days = int(offset_str.rstrip('d'))
                td = timedelta(days=offset_days)
            except ValueError:
                td = timedelta(0)
            val = (datetime.now() + td).strftime(fmt)
            result = result[:match.start()] + val + result[match.end():]

        # Process {{hash length=N}}
        hash_pattern = r'\{\{hash(?:\s+length=(\d+))?\}\}'
        for match in re.finditer(hash_pattern, result):
            length = int(match.group(1)) if match.group(1) else 16
            val = hashlib.sha256(str(random.random()).encode()).hexdigest()[:length]
            result = result[:match.start()] + val + result[match.end():]

        return result

    def _resolve_dict_field(self, field_def: Dict[str, Any]) -> Any:
        """Handle dict field definitions with type/params syntax."""
        # Provider call: { type: "...", ... }
        if "type" in field_def:
            return self._call_provider(field_def)

        # Plain dict
        result = {}
        for k, v in field_def.items():
            result[k] = self._resolve_field(k, v)
        return result

    def _resolve_list_field(self, field_def: List[Any]) -> List[Any]:
        """Handle list field definitions."""
        return [self._resolve_field(f"[{i}]", v) for i, v in enumerate(field_def)]

    def _call_provider(self, field_def: Dict[str, Any]) -> Any:
        """Call the appropriate provider based on type."""
        ptype = field_def.get("type", "static").lower()
        params = {k: v for k, v in field_def.items() if k != "type"}
        # Always include 'type' so providers like BasicProvider can route correctly
        params["type"] = ptype

        try:
            provider = self.registry.get(ptype)
            return provider.generate(**params)
        except Exception as e:
            return f"<{ptype}:{str(e)}>"

    def generate_record(self, schema: Dict[str, Any], index: int = 1) -> Dict[str, Any]:
        """Generate a single record from the schema."""
        record = {}
        fields = schema.get("fields", schema)

        for field_name, field_def in fields.items():
            value = self._resolve_field(field_name, field_def)

            # Handle key templating with {{index}}
            if isinstance(field_name, str) and "{{index}}" in field_name:
                field_name = field_name.replace("{{index}}", str(index))
            if isinstance(field_name, str) and "{{date}}" in field_name:
                field_name = field_name.replace("{{date}}", datetime.now().strftime("%Y%m%d"))

            record[field_name] = value

        return record
