# MockCraft

<p align="center">
  <strong>YAML駆動の構造化テストデータファクトリー</strong><br>
  ゼロ依存Python CLI — YAMLでスキーマを定義し、秒でリアルなデータを生成
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Dependencies-Zero-success.svg" alt="Zero Dependencies">
</p>

---

## 🎉 プロジェクト紹介

MockCraftは、軽量でゼロ依存のPython CLIツールです。YAMLスキーマでデータ構造を定義し、構造化されたモックデータを自動生成します。データベースのシーディング、APIテスト、ベンチマークテスト、開発デモなどに最適です。

## ✨ 主な機能

- **YAML駆動** — 宣言的なスキーマ定義
- **23+ 組み込みプロバイダー** — 名前、メール、電話、住所、IP、URL、UUIDなど
- **ゼロ実行時依存** — Python標準ライブラリのみ（PyYAMLのみ必要）
- **6つの出力フォーマット** — テーブル、JSON、CSV、SQL INSERT、Markdown、YAML
- **再現可能なシード** — 同じシードで同じデータを生成
- **多言語対応** — 日本語(ja_JP)、中国語(zh_CN)、英語(en_US)、韓国語(ko_KR)
- **CLI + Python API** — コマンドラインとライブラリの両方で利用可能

## 🚀 クイックスタート

### インストール

```bash
pip install mockcraft
```

### 最初のデータを生成

YAMLスキーマを作成（`users.yaml`）：

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
```

レコードを生成：

```bash
mockcraft generate users.yaml -n 10
mockcraft generate users.yaml -n 100 --format=json --output=users.json
mockcraft generate users.yaml -n 100 --format=csv --output=users.csv
```

### Python API

```python
from mockcraft import MockCraft

mc = MockCraft(locale="ja_JP")
schema = {
    "fields": {
        "id": {"type": "uuid"},
        "name": {"type": "person"},
        "email": {"type": "email"},
    }
}
records = mc.generate(schema, count=100, seed=42)
```

## 📖 詳細ガイド

### 利用可能なプロバイダー

| タイプ | 説明 | パラメータ |
|--------|------|-----------|
| `person` / `name` | 名前 | `gender`: male/female |
| `email` | メールアドレス | `name`, `domain` |
| `phone` / `mobile` | 電話番号 | — |
| `address` | 住所 | — |
| `int` | 整数 | `min`, `max` |
| `float` | 浮動小数点 | `min`, `max`, `decimals` |
| `bool` | 真偽値 | — |
| `choice` | ランダム選択 | `choices`: [リスト] |
| `uuid` | UUID v4 | — |
| `ipv4` | IPv4アドレス | — |
| `url` | URL | — |
| `datetime` | 日時文字列 | `format`, `offset_days` |
| `sentence` | 文 | `count` |

## 💡 設計思想

1. **Schema as Code** — テストデータ構造をコードと一緒にバージョン管理
2. **Convention over Configuration** — 妥当なデフォルト、最小限のボイラープレート
3. **Zero Runtime Dependencies** — PyYAMLのみ、残りは標準ライブラリ

### ロードマップ

- [ ] カスタムプロバイダープラグインシステム
- [ ] リレーショナルデータ生成（外部キー）
- [ ] JSON Schemaサポート
- [ ] Dockerイメージ

## 📦 ビルドとデプロイ

```bash
git clone https://github.com/gitstq/mockcraft.git
cd mockcraft
pip install -e .
python tests/test_mockcraft.py
```

## 🤝 コントリビューション

[CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

## 📄 ライセンス

MITライセンス — 詳細は [LICENSE](LICENSE) を参照。

---

<p align="center">
  <a href="https://github.com/gitstq">gitstq</a> が ❤️ で作成
</p>
