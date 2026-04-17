"""
MockCraft CLI - Command-line interface.
"""
import sys
import argparse
import importlib.metadata
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mockcraft",
        description="MockCraft - YAML-driven structured test data factory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mockcraft generate schema.yaml -n 100
  mockcraft generate schema.yaml -n 10 --format=csv --output=data.csv
  mockcraft generate schema.yaml -n 5 --format=sql --table=users
  mockcraft list-providers
  mockcraft validate schema.yaml
  echo 'fields: {name: {type: person}}' | mockcraft generate -n 3

Supported formats: table, json, csv, sql, markdown, yaml
        """
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # generate command
    gen = sub.add_parser("generate", help="Generate data from YAML schema", aliases=["gen"])
    gen.add_argument("schema", nargs="?", type=str, help="YAML schema file path")
    gen.add_argument("-n", "--count", type=int, default=1, help="Number of records to generate (default: 1)")
    gen.add_argument("-f", "--format", dest="output_format", default="table",
                     choices=["table","json","csv","sql","markdown","yaml"],
                     help="Output format (default: table)")
    gen.add_argument("-o", "--output", dest="output_file", type=str,
                     help="Output file path (default: stdout)")
    gen.add_argument("-s", "--seed", type=int, help="Random seed for reproducibility")
    gen.add_argument("--start", type=int, default=1, dest="start_index",
                     help="Starting index (default: 1)")
    gen.add_argument("--locale", default="zh_CN",
                     choices=["zh_CN","en_US","ja_JP","ko_KR","zh_TW"],
                     help="Locale for data generation (default: zh_CN)")
    gen.add_argument("--table", default="mock_data",
                     help="Table name for SQL output (default: mock_data)")
    gen.add_argument("-i", "--interactive", action="store_true",
                     help="Interactive YAML schema editor")
    gen.add_argument("-", dest="stdin_schema", action="store_true",
                     help="Read schema from stdin")

    # list-providers command
    sub.add_parser("list-providers", help="List all available data providers", aliases=["lp"])

    # validate command
    val = sub.add_parser("validate", help="Validate a YAML schema file", aliases=["val"])
    val.add_argument("schema", type=str, help="YAML schema file to validate")

    # version
    sub.add_parser("version", help="Show version info", aliases=["v"])

    return parser


def cmd_list_providers(args, mc):
    from mockcraft.providers.registry import ProviderRegistry
    locale = getattr(args, "locale", "zh_CN")
    reg = ProviderRegistry(locale)
    providers = reg.list_providers()
    print(f"\n{'='*50}")
    print(f"  MockCraft Available Providers ({len(providers)} types)")
    print(f"{'='*50}")
    for i, p in enumerate(providers, 1):
        print(f"  {i:>2}. {p}")
    print(f"{'='*50}\n")
    print("Examples:")
    print('  name:     {type: person, gender: male}')
    print('  email:    {type: email}')
    print('  phone:    {type: phone}')
    print('  address:  {type: address}')
    print('  age:      {type: int, min: 18, max: 65}')
    print('  score:    {type: float, min: 0.0, max: 100.0, decimals: 2}')
    print('  online:   {type: bool}')
    print('  id:       {type: uuid}')
    print('  url:      {type: url}')
    print('  created:  {type: datetime, format: "%%Y-%%m-%%d %%H:%%M:%%S"}')


def cmd_validate(args, mc):
    import yaml
    try:
        path = Path(args.schema)
        if not path.exists():
            print(f"❌ Error: File not found: {args.schema}", file=sys.stderr)
            sys.exit(1)
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        # Basic validation
        if not isinstance(data, dict):
            print("❌ Error: Schema must be a YAML dict/object", file=sys.stderr)
            sys.exit(1)
        if "fields" not in data and not any(isinstance(v, (dict, list, str)) for v in data.values()):
            print("⚠️  Warning: Schema has no 'fields' key. Top-level keys will be used as fields.")
        print(f"✅ Schema is valid! ({len(data.get('fields', data))} fields found)")
        print(f"\nTop-level keys: {list(data.keys())}")
        return True
    except yaml.YAMLError as e:
        print(f"❌ YAML Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_generate(args, mc):
    import yaml

    # Load schema
    if args.stdin_schema or (not args.schema):
        schema_data = yaml.safe_load(sys.stdin.read())
    else:
        path = Path(args.schema)
        if not path.exists():
            print(f"❌ Error: File not found: {args.schema}", file=sys.stderr)
            sys.exit(1)
        with open(path, encoding="utf-8") as f:
            schema_data = yaml.safe_load(f)

    if not schema_data:
        print("❌ Error: Empty schema", file=sys.stderr)
        sys.exit(1)

    # Generate
    records = mc.generate(
        schema=schema_data,
        count=args.count,
        start_index=args.start_index,
        seed=args.seed,
    )

    # Format output
    fmt = args.output_format
    if fmt == "sql":
        from mockcraft.formatters import get_formatter
        formatter = get_formatter("sql")
        content = formatter.format_batch(records, table=args.table)
    elif fmt == "json":
        from mockcraft.formatters import get_formatter
        formatter = get_formatter("json")
        content = formatter.format_batch(records)
    elif fmt == "csv":
        from mockcraft.formatters import get_formatter
        formatter = get_formatter("csv")
        content = formatter.format_batch(records)
    elif fmt == "yaml":
        from mockcraft.formatters import get_formatter
        formatter = get_formatter("yaml")
        content = formatter.format_batch(records)
    elif fmt == "markdown" or fmt == "md":
        from mockcraft.formatters import get_formatter
        formatter = get_formatter("markdown")
        content = formatter.format_batch(records)
    else:
        from mockcraft.formatters import get_formatter
        formatter = get_formatter("table")
        content = formatter.format_batch(records)

    # Output
    if args.output_file:
        Path(args.output_file).write_text(content, encoding="utf-8")
        print(f"✅ Generated {len(records)} records → {args.output_file}")
    else:
        print(content)


def cmd_version(args, mc):
    from mockcraft import __version__
    print(f"MockCraft v{__version__}")
    print(f"Python {sys.version.split()[0]}")
    print(f"Author: {importlib.metadata.metadata('mockcraft').get('Author', 'gitstq')}")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    # Determine locale from args or default
    locale = getattr(args, "locale", "zh_CN")

    # Build MockCraft instance
    if args.command in ("generate", "gen", None):
        from mockcraft import MockCraft
        mc = MockCraft(locale=locale)
    else:
        mc = None

    if args.command in ("generate", "gen"):
        cmd_generate(args, mc)
    elif args.command in ("list-providers", "lp"):
        cmd_list_providers(args, mc)
    elif args.command in ("validate", "val"):
        cmd_validate(args, mc)
    elif args.command in ("version", "v"):
        cmd_version(args, mc)
    else:
        # No command: show help
        parser.print_help()


if __name__ == "__main__":
    main()
