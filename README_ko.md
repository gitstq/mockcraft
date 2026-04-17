# MockCraft

<p align="center">
  <strong>YAML 기반 구조화된 테스트 데이터 팩토리</strong><br>
  영종속성 Python CLI — YAML로 스키마를 정의하고, 초 단위로 리얼한 데이터 생성
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Dependencies-Zero-success.svg" alt="Zero Dependencies">
</p>

---

## 🎉 프로젝트 소개

MockCraft는 가볍고 영종속성인 Python CLI 도구입니다. YAML 스키마로 데이터 구조를 정의하고, 구조화된 모의 데이터를 자동 생성합니다. 데이터베이스 시딩, API 테스트, 벤치마크 테스트, 개발 데모 등에 적합합니다.

## ✨ 핵심 기능

- **YAML 기반** — 선언형 스키마 정의
- **23+ 내장 프로바이더** — 이름, 이메일, 전화번호, 주소, IP, URL, UUID 등
- **영 런타임 의존성** — Python 표준 라이브러리만 필요
- **6가지 출력 형식** — 테이블, JSON, CSV, SQL INSERT, Markdown, YAML
- **재현 가능한 시드** — 동일한 시드로 동일한 데이터 생성
- **다국어 지원** — 한국어(ko_KR), 중국어(zh_CN), 영어(en_US), 일본어(ja_JP)
- **CLI + Python API** — 명령줄과 라이브러리 모두 사용 가능

## 🚀 빠른 시작

### 설치

```bash
pip install mockcraft
```

### 첫 데이터 생성

YAML 스키마 생성（`users.yaml`）：

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

레코드 생성：

```bash
mockcraft generate users.yaml -n 10
mockcraft generate users.yaml -n 100 --format=json --output=users.json
```

### Python API

```python
from mockcraft import MockCraft

mc = MockCraft(locale="ko_KR")
schema = {
    "fields": {
        "id": {"type": "uuid"},
        "name": {"type": "person"},
        "email": {"type": "email"},
    }
}
records = mc.generate(schema, count=100, seed=42)
```

## 📖 상세 가이드

### 사용 가능한 프로바이더

| 타입 | 설명 | 파라미터 |
|------|------|---------|
| `person` / `name` | 이름 | `gender`: male/female |
| `email` | 이메일 | `name`, `domain` |
| `phone` / `mobile` | 전화번호 | — |
| `address` | 주소 | — |
| `int` | 정수 | `min`, `max` |
| `float` | 실수 | `min`, `max`, `decimals` |
| `bool` | 불리언 | — |
| `choice` | 랜덤 선택 | `choices`: [목록] |
| `uuid` | UUID v4 | — |
| `datetime` | 날짜시간 문자열 | `format`, `offset_days` |

## 💡 설계 철학

1. **Schema as Code** — 테스트 데이터 구조를 코드와 함께 버전 관리
2. **Convention over Configuration** — 합리적인 기본값, 최소한의 보일러플레이트
3. **영 런타임 의존성** — PyYAML만 필요, 나머지는 표준 라이브러리

## 📦 빌드 및 배포

```bash
git clone https://github.com/gitstq/mockcraft.git
cd mockcraft
pip install -e .
python tests/test_mockcraft.py
```

## 🤝 기여하기

[CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

## 📄 라이선스

MIT 라이선스 — 자세한 내용은 [LICENSE](LICENSE)를 참조.

---

<p align="center">
  <a href="https://github.com/gitstq">gitstq</a>가 ❤️로 제작
</p>
