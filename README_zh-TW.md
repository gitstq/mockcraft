# MockCraft

<p align="center">
  <strong>YAML 驅動的結構化測試資料工廠</strong><br>
  零依賴 Python CLI — 用 YAML 定義資料結構，秒級生成真實測試資料
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Dependencies-Zero-success.svg" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Providers-23+-orange.svg" alt="23+ Providers">
</p>

---

## 🎉 專案介紹

MockCraft 是一個輕量級、零依賴的 Python CLI 工具，透過 YAML Schema 定義資料結構，自動生成結構化的模擬資料。適用於資料庫填充、API 測試、效能基準測試、開發演示等場景 — 無需手寫樣板程式碼。

## ✨ 核心特性

- **YAML 驅動** — 宣告式定義資料結構
- **23+ 內建資料生成器** — 姓名、郵箱、手機號、地址、IP、URL、UUID、時間戳、文字等
- **零執行期依賴** — 僅需 Python 標準庫（加 PyYAML 解析 Schema）
- **6 種輸出格式** — 表格、JSON、CSV、SQL INSERT、Markdown、YAML
- **可再現種子** — 相同種子始終生成相同資料
- **多語言支援** — 簡體中文 (zh_CN)、英文 (en_US)、日文 (ja_JP)、韓文 (ko_KR)、繁體中文 (zh_TW)
- **CLI + Python API** — 命令列或函式庫兩種使用方式
- **串流生成** — 大資料量場景下記憶體友好

## 🚀 快速開始

### 安裝

```bash
pip install mockcraft
```

### 生成第一批資料

建立 YAML Schema（`users.yaml`）：

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
    choices: [北京, 上海, 深圳, 廣州]
  is_active:
    type: bool
  balance:
    type: float
    min: 0
    max: 10000
    decimals: 2
```

生成 10 筆記錄：

```bash
mockcraft generate users.yaml -n 10
```

### Python API 用法

```python
from mockcraft import MockCraft

mc = MockCraft(locale="zh_TW")
schema = {
    "fields": {
        "id": {"type": "uuid"},
        "name": {"type": "person"},
        "email": {"type": "email"},
    }
}
records = mc.generate(schema, count=100, seed=42)
```

## 📖 詳細使用指南

### CLI 命令

```bash
# 生成資料
mockcraft generate <schema.yaml> -n <數量> [-f 格式] [-o 輸出檔案] [-s 種子]

# 查看所有可用的資料生成器
mockcraft list-providers

# 校驗 Schema 檔案
mockcraft validate <schema.yaml>
```

### 可用資料生成器

| 類型 | 說明 | 參數 |
|------|------|------|
| `person` / `name` | 人名 | `gender`: male/female |
| `email` | 電子郵件 | `name`, `domain` |
| `phone` / `mobile` | 手機號碼 | — |
| `address` | 地址 | — |
| `int` | 整數 | `min`, `max` |
| `float` | 浮點數 | `min`, `max`, `decimals` |
| `bool` | 布林值 | — |
| `choice` | 隨機選擇 | `choices`: [列表] |
| `uuid` | UUID v4 | — |
| `ipv4` | IPv4 位址 | — |
| `url` | URL | — |
| `datetime` | 日期時間字串 | `format`, `offset_days` |
| `sentence` | 句子 | `count` |
| `paragraph` | 段落 | `count` |

## 💡 設計思路

1. **Schema 即程式碼** — 測試資料結構與程式碼庫一同版本管理
2. **約定優於配置** — 合理預設值，最小化樣板
3. **零執行期依賴** — 僅 PyYAML 用於解析，其餘全部標準庫
4. **可再現優先** — 基於種子的確定性生成

### 迭代規劃

- [ ] 自訂資料生成器外掛系統
- [ ] 關聯資料生成（外鍵關係）
- [ ] JSON Schema 支援
- [ ] Docker 獨立映像
- [ ] Excel (XLSX) 輸出格式

## 📦 打包與部署

```bash
git clone https://github.com/gitstq/mockcraft.git
cd mockcraft
pip install -e .
python tests/test_mockcraft.py
```

## 🤝 貢獻指南

參見 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📄 開源協議

本專案基於 MIT 協議開源 — 詳見 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  由 <a href="https://github.com/gitstq">gitstq</a> 用 ❤️ 製作
</p>
