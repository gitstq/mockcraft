"""
MockCraft Test Suite - Basic smoke tests.
"""
import sys
from pathlib import Path

# Add parent to path for direct testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from mockcraft import MockCraft
from mockcraft.engine import DataEngine
from mockcraft.providers.registry import ProviderRegistry


def test_import():
    """Test that the package imports correctly."""
    from mockcraft import MockCraft, __version__
    assert __version__ == "1.0.0"
    print(f"✅ Import test passed — MockCraft v{__version__}")


def test_person_provider():
    """Test person name generation."""
    reg = ProviderRegistry("zh_CN")
    provider = reg.get("person")
    name = provider.generate()
    assert name
    assert len(name) >= 2
    print(f"✅ Person provider (zh_CN): {name}")

    reg_en = ProviderRegistry("en_US")
    provider_en = reg_en.get("person")
    name_en = provider_en.generate()
    assert " " in name_en
    print(f"✅ Person provider (en_US): {name_en}")


def test_email_provider():
    """Test email generation."""
    reg = ProviderRegistry("zh_CN")
    provider = reg.get("email")
    email = provider.generate()
    assert "@" in email
    assert "." in email.split("@")[1]
    print(f"✅ Email provider: {email}")


def test_phone_provider():
    """Test phone number generation."""
    reg = ProviderRegistry("zh_CN")
    provider = reg.get("phone")
    phone = provider.generate()
    assert phone.startswith("+86")
    assert len(phone) >= 13
    print(f"✅ Phone provider: {phone}")


def test_address_provider():
    """Test address generation."""
    reg = ProviderRegistry("zh_CN")
    provider = reg.get("address")
    addr = provider.generate()
    assert len(addr) >= 8
    print(f"✅ Address provider: {addr}")


def test_int_provider():
    """Test integer generation."""
    reg = ProviderRegistry()
    provider = reg.get("int")
    val = provider.generate(min=1, max=100)
    assert 1 <= val <= 100
    print(f"✅ Int provider: {val} (range 1-100)")


def test_float_provider():
    """Test float generation."""
    reg = ProviderRegistry()
    provider = reg.get("float")
    val = provider.float_generate(min=0.0, max=1.0, decimals=3)
    assert 0.0 <= val <= 1.0
    print(f"✅ Float provider: {val} (range 0-1, 3 decimals)")


def test_uuid_provider():
    """Test UUID generation."""
    reg = ProviderRegistry()
    provider = reg.get("uuid")
    val = provider.uuid_generate()
    assert len(val) == 36
    assert val.count("-") == 4
    print(f"✅ UUID provider: {val}")


def test_bool_provider():
    """Test boolean generation."""
    reg = ProviderRegistry()
    provider = reg.get("bool")
    val = provider.bool_generate()
    assert isinstance(val, bool)
    print(f"✅ Bool provider: {val}")


def test_network_provider():
    """Test network data generation."""
    reg = ProviderRegistry()
    provider = reg.get("ipv4")
    ip = provider._generate_ipv4()
    parts = ip.split(".")
    assert len(parts) == 4
    print(f"✅ IPv4 provider: {ip}")

    url = provider._generate_url()
    assert "://" in url
    print(f"✅ URL provider: {url}")


def test_time_provider():
    """Test time data generation."""
    reg = ProviderRegistry()
    provider = reg.get("datetime")
    dt = provider.generate(format="%Y-%m-%d %H:%M:%S")
    assert len(dt) == 19
    print(f"✅ DateTime provider: {dt}")


def test_choice_provider():
    """Test choice generation."""
    reg = ProviderRegistry()
    provider = reg.get("choice")
    val = provider.choice_generate(choices=["A", "B", "C"])
    assert val in ["A", "B", "C"]
    print(f"✅ Choice provider: {val}")


def test_text_provider():
    """Test text generation."""
    reg = ProviderRegistry("zh_CN")
    provider = reg.get("sentence")
    text = provider.generate(count=1)
    assert len(text) >= 5
    print(f"✅ Sentence provider (zh_CN): {text[:30]}...")

    reg_en = ProviderRegistry("en_US")
    provider_en = reg_en.get("sentence")
    text_en = provider_en.generate(count=1)
    assert " " in text_en
    print(f"✅ Sentence provider (en_US): {text_en[:30]}...")


def test_basic_workflow():
    """Test the full MockCraft generate workflow."""
    mc = MockCraft(locale="zh_CN")
    schema = {
        "fields": {
            "user_id": {"type": "int", "min": 1000, "max": 9999},
            "name": {"type": "person"},
            "email": {"type": "email"},
            "age": {"type": "int", "min": 18, "max": 60},
            "city": {"type": "choice", "choices": ["北京", "上海", "深圳"]},
            "active": {"type": "bool"},
            "balance": {"type": "float", "min": 0, "max": 1000, "decimals": 2},
            "registered": {"type": "datetime", "format": "%Y-%m-%d"},
        }
    }
    records = mc.generate(schema, count=3, seed=42)
    assert len(records) == 3
    for r in records:
        assert "user_id" in r
        assert "name" in r
        assert "email" in r
        assert "@" in r["email"]
        assert 18 <= r["age"] <= 60
        assert r["city"] in ["北京", "上海", "深圳"]
    print(f"✅ Full workflow: Generated {len(records)} records")
    for r in records:
        print(f"   → {r['name']} <{r['email']}> age={r['age']} city={r['city']}")


def test_seed_reproducibility():
    """Test that same seed produces same results."""
    mc1 = MockCraft()
    mc2 = MockCraft()
    schema = {"fields": {"v": {"type": "int", "min": 0, "max": 10000}}}
    r1 = mc1.generate(schema, count=5, seed=12345)
    r2 = mc2.generate(schema, count=5, seed=12345)
    assert [rec["v"] for rec in r1] == [rec["v"] for rec in r2]
    print(f"✅ Seed reproducibility: same seed = same sequence")


def test_all_providers_registered():
    """Test all providers are registered."""
    reg = ProviderRegistry()
    providers = reg.list_providers()
    expected = ["address","bool","choice","date","datetime","email","float","fullname","int","ipv4",
                "ipv6","name","person","phone","sentence","static","timestamp","url","user_agent","uuid","word"]
    for ep in expected:
        assert ep in providers, f"Missing provider: {ep}"
    print(f"✅ All {len(providers)} providers registered: {providers}")


def test_formatters():
    """Test output formatters."""
    from mockcraft.formatters import get_formatter
    records = [
        {"id": 1, "name": "Alice", "score": 95.5},
        {"id": 2, "name": "Bob", "score": 87.3},
    ]
    json_out = get_formatter("json").format_batch(records)
    assert '"id": 1' in json_out
    assert '"name": "Alice"' in json_out
    print(f"✅ JSON formatter: {len(json_out)} chars")

    csv_out = get_formatter("csv").format_batch(records)
    assert "id,name,score" in csv_out
    print(f"✅ CSV formatter: {len(csv_out)} chars")

    md_out = get_formatter("markdown").format_batch(records)
    assert "Alice" in md_out
    print(f"✅ Markdown formatter: {len(md_out)} chars")


def run_all():
    print("\n" + "="*60)
    print("  MockCraft Test Suite")
    print("="*60 + "\n")
    tests = [
        test_import,
        test_person_provider,
        test_email_provider,
        test_phone_provider,
        test_address_provider,
        test_int_provider,
        test_float_provider,
        test_uuid_provider,
        test_bool_provider,
        test_network_provider,
        test_time_provider,
        test_choice_provider,
        test_text_provider,
        test_basic_workflow,
        test_seed_reproducibility,
        test_all_providers_registered,
        test_formatters,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1
    print(f"\n{'='*60}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'='*60}\n")
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
