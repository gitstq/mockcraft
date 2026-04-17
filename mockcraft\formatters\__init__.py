"""
MockCraft Formatters - output in various formats.
"""
import json
import csv
import io
from typing import Any, Dict, List


class TableFormatter:
    """Pretty-print records as ASCII tables."""

    def format_record(self, record: Dict[str, Any]) -> str:
        if not record:
            return ""
        keys = list(record.keys())
        col_widths = {k: max(len(str(k)), len(str(record[k]))) for k in keys}
        sep = "+" + "+".join("-" * (col_widths[k] + 2) for k in keys) + "+"
        rows = [sep]
        rows.append("|" + "|".join(f" {k:<{col_widths[k]}} " for k in keys) + "|")
        rows.append(sep)
        rows.append("|" + "|".join(f" {str(record[k]):<{col_widths[k]}} " for k in keys) + "|")
        rows.append(sep)
        return "\n".join(rows)

    def format_batch(self, records: List[Dict[str, Any]], **kwargs) -> str:
        if not records:
            return ""
        keys = list(records[0].keys())
        col_widths = {k: len(str(k)) for k in keys}
        for r in records:
            for k in keys:
                col_widths[k] = max(col_widths[k], len(str(r.get(k, ""))))

        sep = "+" + "+".join("-" * (col_widths[k] + 2) for k in keys) + "+"
        lines = [sep]
        lines.append("|" + "|".join(f" {k:<{col_widths[k]}} " for k in keys) + "|")
        lines.append(sep)
        for r in records:
            lines.append("|" + "|".join(f" {str(r.get(k, '')):<{col_widths[k]}} " for k in keys) + "|")
        lines.append(sep)
        return "\n".join(lines)


class JsonFormatter:
    """Format records as JSON."""

    def format_record(self, record: Dict[str, Any], **kwargs) -> str:
        return json.dumps(record, ensure_ascii=False, indent=2)

    def format_batch(self, records: List[Dict[str, Any]], pretty: bool = True, **kwargs) -> str:
        if pretty:
            return json.dumps(records, ensure_ascii=False, indent=2)
        return json.dumps(records, ensure_ascii=False)


class CsvFormatter:
    """Format records as CSV."""

    def format_record(self, record: Dict[str, Any], **kwargs) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(record.keys()))
        writer.writeheader()
        writer.writerow(record)
        return output.getvalue()

    def format_batch(self, records: List[Dict[str, Any]], **kwargs) -> str:
        if not records:
            return ""
        output = io.StringIO()
        fieldnames = list(records[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        return output.getvalue()


class SqlFormatter:
    """Format records as SQL INSERT statements."""

    def format_record(self, record: Dict[str, Any], table: str = "mock_data", **kwargs) -> str:
        cols = list(record.keys())
        vals = [self._escape_sql(v) for v in record.values()]
        cols_str = ", ".join(f"`{c}`" for c in cols)
        vals_str = ", ".join(vals)
        return f"INSERT INTO `{table}` ({cols_str}) VALUES ({vals_str});"

    def format_batch(self, records: List[Dict[str, Any]], table: str = "mock_data", **kwargs) -> str:
        lines = [self.format_record(r, table=table) for r in records]
        return "\n".join(lines)

    def _escape_sql(self, val: Any) -> str:
        if val is None:
            return "NULL"
        if isinstance(val, bool):
            return "TRUE" if val else "FALSE"
        if isinstance(val, (int, float)):
            return str(val)
        s = str(val).replace("'", "''")
        return f"'{s}'"


class MarkdownFormatter:
    """Format records as Markdown table."""

    def format_record(self, record: Dict[str, Any], **kwargs) -> str:
        return self.format_batch([record], **kwargs)

    def format_batch(self, records: List[Dict[str, Any]], **kwargs) -> str:
        if not records:
            return ""
        keys = list(records[0].keys())
        lines = []
        lines.append("| " + " | ".join(keys) + " |")
        lines.append("|" + "|".join(" --- " for _ in keys) + "|")
        for r in records:
            vals = [str(r.get(k, "")) for k in keys]
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)


class YamlFormatter:
    """Format records as YAML."""

    def format_record(self, record: Dict[str, Any], **kwargs) -> str:
        import yaml
        return yaml.dump(record, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def format_batch(self, records: List[Dict[str, Any]], **kwargs) -> str:
        import yaml
        return yaml.dump(records, allow_unicode=True, default_flow_style=False, sort_keys=False)


_FORMATTERS = {
    "table": TableFormatter,
    "json": JsonFormatter,
    "csv": CsvFormatter,
    "sql": SqlFormatter,
    "markdown": MarkdownFormatter,
    "md": MarkdownFormatter,
    "yaml": YamlFormatter,
    "text": TableFormatter,
}


def get_formatter(name: str):
    """Get a formatter instance by name."""
    cls = _FORMATTERS.get(name.lower())
    if cls is None:
        raise ValueError(f"Unknown format: {name}. Available: {list(_FORMATTERS.keys())}")
    return cls()
