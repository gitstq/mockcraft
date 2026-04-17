# MockCraft

<p align="center">
  <strong>YAML 驱动的结构化测试数据工厂</strong><br>
  零依赖 Python CLI — 用 YAML 定义数据结构，秒级生成真实测试数据
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Dependencies-Zero-success.svg" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Providers-23+-orange.svg" alt="23+ Providers">
</p>

---

## 🎉 项目介绍

MockCraft 是一个轻量级、零依赖的 Python CLI 工具，通过 YAML Schema 定义数据结构，自动生成结构化的模拟数据。适用于数据库填充、API 测试、性能基准测试、开发演示等场景 — 无需手写样板代码。

**与 Faker 的区别：** Faker 是生成单个伪造值的 Python 库。MockCraft 是**数据工厂** — 在 YAML 中定义完整的数据结构，一条命令生成数百条一致、真实的记录。

## ✨ 核心特性

- **YAML 驱动** — 声明式定义数据结构
- **23+ 内置数据生成器** — 姓名、邮箱、手机号、地址、IP、URL、UUID、时间戳、文本等
- **零运行时依赖** — 仅需 Python 标准库（加 PyYAML 解析 Schema）
- **6 种输出格式** — 表格、JSON、CSV、SQL INSERT、Markdown、YAML
- **可复现种子** — 相同种子始终生成相同数据
- **多语言支持** — 简体中文 (zh_CN)、英文 (en_US)、日文 (ja_JP)、韩文 (ko_KR)、繁体中文 (zh_TW)
- **CLI + Python API** — 命令行或库两种使用方式
- **流式生成** — 大数据量场景下内存友好

## 🚀 快速开始

### 安装

```bash
pip install mockcraft
```

或从源码安装：

```bash
git clone https://github.com/gitstq/mockcraft.git
cd mockcraft
pip install -e .
```

### 生成第一批数据

创建 YAML Schema（`users.yaml`）：

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
    choices: [北京, 上海, 深圳, 广州]
  is_active:
    type: bool
  balance:
    type: float
    min: 0
    max: 10000
    decimals: 2
```

生成 10 条记录：

```bash
mockcraft generate users.yaml -n 10
```

导出为不同格式：

```bash
# JSON 格式
mockcraft generate users.yaml -n 100 --format=json --output=users.json

# CSV 格式
mockcraft generate users.yaml -n 100 --format=csv --output=users.csv

# SQL INSERT 语句
mockcraft generate users.yaml -n 100 --format=sql --table=t_users --output=users.sql

# Markdown 表格
mockcraft generate users.yaml -n 10 --format=markdown
```

## 📖 详细使用指南

### CLI 命令

```bash
# 生成数据
mockcraft generate <schema.yaml> -n <数量> [-f 格式] [-o 输出文件] [-s 种子]

# 查看所有可用的数据生成器
mockcraft list-providers

# 校验 Schema 文件
mockcraft validate <schema.yaml>

# 查看版本
mockcraft version
```

### CLI 参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--count` | `-n` | 生成记录数量 | 1 |
| `--format` | `-f` | 输出格式 (table/json/csv/sql/markdown/yaml) | table |
| `--output` | `-o` | 输出文件路径（省略则输出到终端） | stdout |
| `--seed` | `-s` | 随机种子，用于数据复现 | 随机 |
| `--locale` | | 数据语言 (zh_CN/en_US/ja_JP/ko_KR/zh_TW) | zh_CN |
| `--table` | | SQL 表名 | mock_data |

### 可用数据生成器

| 类型 | 说明 | 参数 |
|------|------|------|
| `person` / `name` / `fullname` | 人名 | `gender`: male/female |
| `email` | 电子邮箱 | `name`, `domain` |
| `phone` / `mobile` | 手机号码 | — |
| `address` | 地址 | — |
| `int` | 整数 | `min`, `max` |
| `float` | 浮点数 | `min`, `max`, `decimals` |
| `bool` | 布尔值 | — |
| `choice` | 随机选择 | `choices`: [列表] |
| `uuid` | UUID v4 | — |
| `ipv4` | IPv4 地址 | — |
| `ipv6` | IPv6 地址 | — |
| `url` | URL | — |
| `user_agent` | 浏览器 UA | — |
| `datetime` | 日期时间字符串 | `format`, `offset_days` |
| `date` | 日期字符串 | `format`, `offset_days` |
| `timestamp` | Unix 时间戳 | `offset_seconds` |
| `sentence` | 句子 | `count` |
| `paragraph` | 段落 | `count` |
| `word` | 单词 | — |
| `static` | 静态值 | `value` |

### Python API 用法

```python
from mockcraft import MockCraft

mc = MockCraft(locale="zh_CN")

# 内联定义 Schema
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

# 生成 100 条记录
records = mc.generate(schema, count=100, seed=42)

# 流式生成（内存友好）
for record in mc.generate_stream(schema, count=100000):
    process(record)

# 导出到文件
mc.export(records, "output.json", format="json")
```

### 模板表达式

MockCraft 支持在字符串字段中使用 `{{表达式}}` 语法：

```yaml
fields:
  username: "{{person}}_{{random.int 100 999}}"
  created_date: "注册于 {{date format='%Y-%m-%d'}}"
  unique_id: "{{random.uuid}}"
```

## 💡 设计思路与迭代规划

1. **Schema 即代码** — 测试数据结构与代码库一同版本管理
2. **约定优于配置** — 合理默认值，最小化样板
3. **零运行时依赖** — 仅 PyYAML 用于解析，其余全部标准库
4. **可复现优先** — 基于种子的确定性生成，确保测试一致性
5. **CLI 原生** — 专为终端工作流、CI/CD 管道和 Shell 脚本设计

### 迭代规划

- [ ] 自定义数据生成器插件系统
- [ ] 关联数据生成（外键关系）
- [ ] JSON Schema 支持
- [ ] GUI Schema 构建器（Web）
- [ ] Docker 独立镜像
- [ ] Excel (XLSX) 输出格式

## 📦 打包与部署

### 从 PyPI 安装（计划中）

```bash
pip install mockcraft
```

### 从源码安装

```bash
git clone https://github.com/gitstq/mockcraft.git
cd mockcraft
pip install -e .

# 安装开发依赖
pip install -e ".[dev]"
```

### 构建分发包

```bash
pip install build
python -m build
```

### 运行测试

```bash
python tests/test_mockcraft.py
```

## 🤝 贡献指南

参见 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献规范。

## 📄 开源协议

本项目基于 MIT 协议开源 — 详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  由 <a href="https://github.com/gitstq">gitstq</a> 用 ❤️ 制作
</p>
