# Contributing to MockCraft

Thanks for your interest in contributing! This document provides guidelines for contributing to MockCraft.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
4. Install in development mode: `pip install -e ".[dev]"`
5. Run tests: `python tests/test_mockcraft.py`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Write code and tests
3. Ensure all tests pass: `python tests/test_mockcraft.py`
4. Commit with conventional commits: `git commit -m "feat: add new provider"`
5. Push to your fork: `git push origin feature/your-feature`
6. Create a Pull Request

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code refactoring
- `test:` Adding/updating tests
- `chore:` Build/config changes

## Adding a New Provider

1. Create a new file in `mockcraft/providers/` (e.g., `company.py`)
2. Implement a class with a `generate(**kwargs)` method
3. Register it in `mockcraft/providers/registry.py`
4. Add tests in `tests/test_mockcraft.py`
5. Update documentation

## Code Style

- Python 3.8+ compatible
- Follow PEP 8
- Add docstrings to public functions/classes
- Maximum line length: 100 characters

## Reporting Issues

Please include:
- MockCraft version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
