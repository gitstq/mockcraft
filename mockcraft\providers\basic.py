"""
MockCraft Basic Provider - uuid, bool, choice, static.
"""
import random
import uuid


class BasicProvider:
    """Generates basic data types: uuid, bool, choice, static."""

    def generate(self, value=None, choices=None, **kwargs):
        """Route to the appropriate sub-generator based on kwargs."""
        ptype = (kwargs.get("type") or "static").lower()
        # bool type
        if ptype == "bool":
            return self.bool_generate()
        # uuid type
        if ptype == "uuid":
            return self.uuid_generate()
        # choice type
        if choices is not None:
            return self.choice_generate(choices)
        # static value
        return value

    def uuid_generate(self, **kwargs) -> str:
        return str(uuid.uuid4())

    def bool_generate(self, **kwargs) -> bool:
        return random.choice([True, False])

    def choice_generate(self, choices: list = None, **kwargs):
        if not choices:
            return None
        if isinstance(choices, str):
            choices = [c.strip() for c in choices.split(",")]
        return random.choice(choices)
