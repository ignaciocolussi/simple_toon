# Contributing to simple-toon

Thank you for considering contributing to simple-toon! This guide will help you get started.

## Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/simple_toon.git
   cd simple_toon
   ```

3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes
- Write code following the project style
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Run Quality Checks

**Format code:**
```bash
black toon_parser/ tests/
```

**Lint code:**
```bash
ruff check toon_parser/ tests/
```

**Type check:**
```bash
mypy toon_parser/
```

**Run tests:**
```bash
pytest --cov=toon_parser --cov-report=term-missing
```

**Run all checks:**
```bash
# This runs automatically with pre-commit, but you can run manually:
pre-commit run --all-files
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "Description of changes"
```

Commit messages should:
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issue numbers when applicable (#123)

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Style Guidelines

### Python Style
- Follow PEP 8 (enforced by black and ruff)
- Line length: 100 characters
- Use type hints for all functions
- Write docstrings for public APIs

**Example:**
```python
def parse_value(value: str) -> Union[int, float, bool, str, None]:
    """Parse a string value and infer its type.

    Args:
        value: The string value to parse

    Returns:
        The parsed value with inferred type

    Examples:
        >>> parse_value("123")
        123
        >>> parse_value("true")
        True
    """
    # Implementation here
```

### Testing
- Write tests for all new features
- Aim for >85% code coverage
- Use descriptive test names
- Test edge cases and error conditions

**Example:**
```python
def test_parse_with_empty_array():
    """Test parsing TOON with empty array."""
    toon = "users[0]{id,name}:"
    result = parse(toon)
    assert result == {"users": []}
```

## Project Structure

```
simple_toon/
├── toon_parser/          # Main package
│   ├── __init__.py       # Public API exports
│   ├── parser.py         # TOON → JSON parser
│   ├── serializer.py     # JSON → TOON serializer
│   ├── advanced.py       # Advanced features
│   ├── schema.py         # Schema validation
│   ├── io.py             # File I/O utilities
│   ├── streaming.py      # Streaming serializer
│   └── oo_api.py         # Object-oriented API
├── tests/                # Test suite
│   ├── test_parser.py
│   ├── test_serializer.py
│   └── ...
├── .github/              # GitHub configs
│   ├── workflows/        # CI/CD workflows
│   └── ISSUE_TEMPLATE/   # Issue templates
└── pyproject.toml        # Package configuration
```

## Testing Multiple Python Versions

The project supports Python 3.8 through 3.12. To test locally:

**Using pyenv:**
```bash
pyenv install 3.8 3.9 3.10 3.11 3.12
pyenv local 3.8 3.9 3.10 3.11 3.12
```

**Using tox (optional):**
```bash
pip install tox
tox
```

## Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/)
- Add docstrings to new functions/classes
- Update examples if API changes

## Release Process

Maintainers handle releases, but the process is:

1. Update version in `pyproject.toml` and `__init__.py`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v0.2.1`
4. Push tag: `git push origin v0.2.1`
5. Create GitHub release (triggers automatic PyPI publish)

## Getting Help

- **Questions?** Open a [Discussion](https://github.com/ignaciocolussi/simple_toon/discussions)
- **Bug?** Open an [Issue](https://github.com/ignaciocolussi/simple_toon/issues)
- **Feature idea?** Open a [Feature Request](https://github.com/ignaciocolussi/simple_toon/issues/new?template=feature_request.md)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project
- Show empathy towards other community members

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- GitHub contributors page
- Release notes for their contributions
- README (for significant contributions)

Thank you for contributing! 🎉
