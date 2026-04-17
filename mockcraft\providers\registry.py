"""
MockCraft Provider Registry.
Central registry for all data provider types.
"""
from typing import Any, Dict, Optional


class ProviderRegistry:
    """Registry that maps provider type names to provider instances."""

    def __init__(self, locale: str = "zh_CN"):
        self.locale = locale
        self._providers: Dict[str, Any] = {}
        self._init_providers()

    def _init_providers(self):
        """Initialize all built-in providers."""
        from .person import PersonProvider
        from .contact import ContactProvider
        from .text import TextProvider
        from .number import NumberProvider
        from .network import NetworkProvider
        from .time_data import TimeProvider
        from .basic import BasicProvider

        self.register("person", PersonProvider(self.locale))
        self.register("name", PersonProvider(self.locale))
        self.register("fullname", PersonProvider(self.locale))
        # Each ContactProvider instance has a default type so generate() returns the right kind
        self.register("email", ContactProvider(self.locale, default_type="email"))
        self.register("phone", ContactProvider(self.locale, default_type="phone"))
        self.register("address", ContactProvider(self.locale, default_type="address"))
        self.register("mobile", ContactProvider(self.locale, default_type="phone"))
        self.register("sentence", TextProvider(self.locale))
        self.register("paragraph", TextProvider(self.locale))
        self.register("word", TextProvider(self.locale))
        self.register("int", NumberProvider())
        self.register("float", NumberProvider())
        self.register("uuid", BasicProvider())
        self.register("bool", BasicProvider())
        self.register("choice", BasicProvider())
        self.register("static", BasicProvider())
        self.register("ipv4", NetworkProvider())
        self.register("ipv6", NetworkProvider())
        self.register("url", NetworkProvider())
        self.register("user_agent", NetworkProvider())
        self.register("datetime", TimeProvider())
        self.register("date", TimeProvider())
        self.register("timestamp", TimeProvider())

    def register(self, name: str, provider):
        """Register a new provider."""
        self._providers[name.lower()] = provider

    def get(self, name: str):
        """Get a provider by name."""
        name = name.lower()
        if name not in self._providers:
            raise ValueError(f"Unknown provider type: {name}")
        return self._providers[name]

    def list_providers(self) -> list:
        """List all registered provider names."""
        return sorted(self._providers.keys())
