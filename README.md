# MockCraft

<p align="center">
  <strong>YAML-driven structured test data factory</strong><br>
  Zero-dependency Python CLI — define your schema in YAML, get realistic data in seconds
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Dependencies-Zero-success.svg" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Providers-23+-orange.svg" alt="23+ Providers">
</p>

---

## 🎉 What is MockCraft?

MockCraft is a lightweight, zero-dependency Python CLI tool that generates structured fake data from YAML schemas. It's designed for developers who need realistic test data for database seeding, API testing, benchmarking, and development demos — without writing boilerplate code.

**Key difference from Faker:** Faker is a Python library for generating individual fake values. MockCraft is a **data factory** — define your entire data structure once in YAML, and generate hundreds of consistent, realistic records in one command.

## ✨ Core Features

- **YAML-Driven Schema** — Define data structures declaratively in YAML
- **23+ Built-in Providers** — Names, emails, phones, addresses, IPs, URLs, UUIDs, timestamps, text, and more
- **Zero Dependencies** — Only Python stdlib required (plus PyYAML for schema parsing)
- **6 Output Formats** — Table, JSON, CSV, SQL INSERT, Markdown, YAML
- **Reproducible Seeds** — Same seed always produces the same data
- **Multi-Locale Support** — Chinese (zh_CN), English (en_US), Japanese (ja_JP), Korean (ko_KR), Traditional Chinese (zh_TW)
- **CLI + Python API** — Use from command line or import as a library
- **Streaming Generator** — Memory-efficient for large datasets

## 🚀 Quick Start

### Install

```bash
pip install mockcraft
```

Or install from source:

```bash
git clone https://github.com/gitstq/mockcraft.git
cd mockcraft
pip install -e .
```

### Generate Your First Data

Create a YAML schema (`users.yaml`):

```yaml
fields:
  user_id:
    type: int
    min: 1000
    max: 9999
  name:
    type: person
  email:
    type: email
  age:
    type: int
    min: 18
    max: 65
  city:
    type: choice
    choices: [Beijing, Shanghai, Shenzhen, Guangzhou]
  is_active:
    type: bool
  balance:
    type: float
    min: 0
    max: 10000
    decimals: 2
```

Generate 10 records:

```bash
mockcraft generate users.yaml -n 10
```

Export to different formats:

```bash
# JSON
mockcraft generate users.yaml -n 100 --format=json --output=users.json

# CSV
mockcraft generate users.yaml -n 100 --format=csv --output=users.csv

# SQL INSERT statements
mockcraft generate users.yaml -n 100 --format=sql --table=t_users --output=users.sql

# Markdown table
mockcraft generate users.yaml -n 10 --format=markdown
```

## 📖 Detailed Guide

### CLI Commands

```bash
# Generate data
mockcraft generate <schema.yaml> -n <count> [-f format] [-o output] [-s seed]

# List all available providers
mockcraft list-providers

# Validate a schema file
mockcraft validate <schema.yaml>

# Show version
mockcraft version
```

### CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--count` | `-n` | Number of records | 1 |
| `--format` | `-f` | Output format (table/json/csv/sql/markdown/yaml) | table |
| `--output` | `-o` | Output file path (stdout if omitted) | stdout |
| `--seed` | `-s` | Random seed for reproducibility | random |
| `--locale` | | Data locale (zh_CN/en_US/ja_JP/ko_KR/zh_TW) | zh_CN |
| `--table` | | SQL table name | mock_data |

### Available Providers

| Type | Description | Parameters |
|------|-------------|------------|
| `person` / `name` / `fullname` | Person name | `gender`: male/female |
| `email` | Email address | `name`, `domain` |
| `phone` / `mobile` | Phone number | — |
| `address` | Street address | — |
| `int` | Integer | `min`, `max` |
| `float` | Float number | `min`, `max`, `decimals` |
| `bool` | Boolean | — |
| `choice` | Random choice | `choices`: [list] |
| `uuid` | UUID v4 | — |
| `ipv4` | IPv4 address | — |
| `ipv6` | IPv6 address | — |
| `url` | URL | — |
| `user_agent` | Browser User-Agent | — |
| `datetime` | Datetime string | `format`, `offset_days` |
| `date` | Date string | `format`, `offset_days` |
| `timestamp` | Unix timestamp | `offset_seconds` |
| `sentence` | Sentences | `count` |
| `paragraph` | Paragraph | `count` |
| `word` | Single word | — |
| `static` | Static value | `value` |

### Python API Usage

```python
from mockcraft import MockCraft

mc = MockCraft(locale="zh_CN")

# Define schema inline
schema = {
    "fields": {
        "id": {"type": "uuid"},
        "name": {"type": "person"},
        "email": {"type": "email"},
        "score": {"type": "float", "min": 0, "max": 100, "decimals": 1},
        "passed": {"type": "bool"},
        "created_at": {"type": "datetime", "format": "%Y-%m-%d %H:%M:%S"},
    }
}

# Generate 100 records
records = mc.generate(schema, count=100, seed=42)

# Stream generate (memory efficient)
for record in mc.generate_stream(schema, count=100000):
    process(record)

# Export to file
mc.export(records, "output.json", format="json")
```

### Template Expressions

MockCraft supports inline `{{expression}}` syntax in string fields:

```yaml
fields:
  username: "{{person}}_{{random.int 100 999}}"
  created_date: "User created on {{date format='%Y-%m-%d'}}"
  unique_id: "{{random.uuid}}"
```

## 💡 Design Philosophy

1. **Schema as Code** — Your test data structure is version-controlled alongside your codebase
2. **Convention over Configuration** — Sensible defaults, minimal boilerplate
3. **Zero Runtime Dependencies** — Only PyYAML for parsing; everything else is stdlib
4. **Reproducibility First** — Seed-based generation for deterministic testing
5. **CLI-Native** — Designed for terminal workflows, CI/CD pipelines, and shell scripting

### Roadmap

- [ ] Custom provider plugin system
- [ ] Relational data generation (foreign keys)
- [ ] JSON Schema support
- [ ] GUI schema builder (web)
- [ ] Docker image for standalone generation
- [ ] Excel (XLSX) output format

## 📦 Build & Deploy

### Install from PyPI (planned)

```bash
pip install mockcraft
```

### Install from Source

```bash
git clone https://github.com/gitstq/mockcraft.git
cd mockcraft
pip install -e .

# With dev dependencies
pip install -e ".[dev]"
```

### Build Distribution

```bash
pip install build
python -m build
```

### Run Tests

```bash
python tests/test_mockcraft.py
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
