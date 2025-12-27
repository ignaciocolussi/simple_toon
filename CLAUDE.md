# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python parser and serializer for **TOON (Token-Oriented Object Notation)**, a compact data format designed to reduce LLM token consumption by 30-60% compared to JSON while maintaining lossless conversion.

TOON is optimized for uniform arrays of objects (tabular/semi-structured data) and uses:
- YAML-style indentation for nesting
- CSV-style tabular layout for arrays
- Explicit schema declarations with `[N]` length and `{field1,field2}` headers

## TOON Format Specification

### Syntax Rules

```
arrayName[count]{field1,field2,field3}:
  value1,value2,value3
  value1,value2,value3
```

**Key elements:**
- `arrayName[N]` — declares array with N elements
- `{field1,field2,...}` — defines column headers (declared once)
- `:` — terminates header line
- Comma-separated values matching header order
- Indentation indicates nesting depth
- String values with special characters must be quoted
- Unquoted values are inferred as numbers/booleans

### Example Conversion

**JSON:**
```json
{
  "users": [
    {"id": 1, "name": "Alice", "active": true},
    {"id": 2, "name": "Bob", "active": false}
  ]
}
```

**TOON:**
```
users[2]{id,name,active}:
  1,Alice,true
  2,Bob,false
```

## Project Structure

```
/
├── toon_parser/          # Main package
│   ├── __init__.py       # Public API exports
│   ├── parser.py         # TOON → JSON parser
│   ├── serializer.py     # JSON → TOON serializer
│   └── advanced.py       # Advanced parsing features
│
├── tests/                # Test suite
│   └── ...
│
├── examples/             # Usage examples
│   └── ...
│
├── pyproject.toml        # Package configuration
├── setup.py              # Setup script
└── CHANGELOG.md          # Version history
```

## Development Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=toon_parser

# Format code
black toon_parser/ tests/

# Lint code
ruff check toon_parser/ tests/

# Type check
mypy toon_parser/

# Build package
python -m build

# Publish to PyPI
twine upload dist/*
```

## Implementation Architecture

### Core Components

The implementation provides:

1. **Parser (TOON → JSON)**
   - Header line parser: extract array name, count, and field names
   - Row tokenizer: split CSV values while respecting quoted strings
   - Type inference: convert unquoted values to appropriate types (number, boolean, null)
   - Indentation handler: track nesting levels for hierarchical data
   - Quote escape handler: properly handle escaped quotes within strings

2. **Serializer (JSON → TOON)**
   - Schema detector: identify uniform array structures
   - Header generator: create `[N]{fields}` declarations
   - Value formatter: quote strings with special characters, leave primitives unquoted
   - Indentation manager: apply proper spacing for nested structures
   - Deterministic output: ensure consistent formatting for same input

### Key Design Decisions

- **Lossless conversion**: Must support perfect round-trip (JSON → TOON → JSON)
- **Deterministic output**: Same JSON input always produces identical TOON output
- **Type preservation**: Maintain distinction between strings, numbers, booleans, and null
- **Error handling**: Provide clear error messages for malformed TOON input
- **Performance**: Optimize for large uniform arrays (primary use case)

### Testing Strategy

- **Round-trip tests**: Verify JSON → TOON → JSON produces identical results
- **Edge cases**: Empty arrays, null values, nested objects, special characters in strings
- **Token counting**: Benchmark token reduction vs JSON (target: 30-60% savings)
- **Accuracy tests**: If applicable, measure LLM parsing accuracy of generated TOON
- **Comprehensive coverage**: Aim for high test coverage across all modules

## Reference Implementations

Existing TOON libraries (for reference, not dependencies):
- **TypeScript**: `@toon-format/toon` (official reference implementation)
- **Python**: Check npm/PyPI for community implementations
- **Spec**: https://github.com/toon-format/spec

## API Design

```python
def parse(toon: str) -> Any:
    """Parse TOON string into Python object."""
    ...

def stringify(json_obj: Any) -> str:
    """Convert Python object to TOON string."""
    ...
```

## Semantic Versioning (SemVer)

This project follows [Semantic Versioning 2.0.0](https://semver.org/).

### Version Format

**MAJOR.MINOR.PATCH** (e.g., `1.2.3`)

- **MAJOR**: Incompatible API changes (breaking changes)
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

### When to Bump Versions

#### MAJOR version (breaking changes):
- Changes to public API function signatures (`parse()`, `stringify()`)
- Changes to TOON format specification that break parsing of existing valid TOON
- Removal of public APIs or exports
- Changes to return value structure that could break user code
- Changes to error handling behavior (new exceptions, changed error types)
- Minimum Python version requirements

#### MINOR version (new features):
- New public APIs or functions
- New optional parameters with defaults
- Performance improvements without API changes
- Extended TOON format support (backward-compatible additions)
- New error messages or warnings (non-breaking)

#### PATCH version (bug fixes):
- Bug fixes that restore documented behavior
- Documentation updates
- Internal refactoring with no API changes
- Dependency updates (non-breaking)
- Test improvements

### Version Update Locations

When bumping versions, update these files:

- [`toon_parser/__init__.py`](toon_parser/__init__.py) — `__version__` variable
- [`pyproject.toml`](pyproject.toml) — `version` field in `[project]` section

### Pre-release Versions

For testing before stable releases:

- **Alpha**: `1.0.0-alpha.1` — Early development, unstable API
- **Beta**: `1.0.0-beta.1` — Feature complete, testing phase
- **Release Candidate**: `1.0.0-rc.1` — Final testing before stable release

### Version Bump Checklist

Before releasing a new version:

1. ✅ Update version numbers in all relevant files
2. ✅ Update CHANGELOG.md with changes since last release
3. ✅ Run full test suite (`pytest --cov=toon_parser`)
4. ✅ Verify round-trip compatibility with previous versions
5. ✅ Build package successfully (`python -m build`)
6. ✅ Tag git commit with version (e.g., `v1.2.3`)
7. ✅ Publish to PyPI (`twine upload dist/*`)
8. ✅ Create GitHub release with release notes

### Breaking Change Examples

**Examples that require MAJOR version bump:**

```python
# Breaking: Changed return type
- def parse(toon: str) -> dict
+ def parse(toon: str) -> ParseResult

# Breaking: Removed function
- def parse_stream(stream: IO) -> Any

# Breaking: Changed parameter requirements
- def stringify(json_obj: Any, indent: int = 2) -> str
+ def stringify(json_obj: Any, options: StringifyOptions) -> str

# Breaking: Changed exception types
- raises ValueError for parse errors
+ raises ToonParseError for parse errors
```

**Examples that allow MINOR version bump:**

```python
# New: Added optional parameter with default
- def stringify(json_obj: Any, indent: int = 2) -> str
+ def stringify(json_obj: Any, indent: int = 2, compact: bool = False) -> str

# New: Added new function
+ def validate(toon: str) -> bool

# New: Added new optional feature
+ def parse(toon: str, strict: bool = False) -> Any
```

## Performance Considerations

- TOON is optimized for **uniform arrays** (e.g., logs, user lists, analytics events)
- For deeply nested non-uniform data, JSON may be more efficient
- Header definition has fixed cost; per-row savings compound with dataset size
- Quote handling is critical for performance (avoid regex where possible)
