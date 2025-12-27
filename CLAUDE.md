# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dual-language (JavaScript/TypeScript + Python) parser and serializer for **TOON (Token-Oriented Object Notation)**, a compact data format designed to reduce LLM token consumption by 30-60% compared to JSON while maintaining lossless conversion.

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

This is a **monorepo** containing two separate packages:

```
/
├── js/                    # JavaScript/TypeScript package (npm)
│   ├── src/
│   │   ├── parser.ts     # TOON → JSON parser
│   │   ├── serializer.ts # JSON → TOON serializer
│   │   └── index.ts      # Public API exports
│   ├── tests/
│   ├── package.json
│   └── tsconfig.json
│
├── python/                # Python package (pip)
│   ├── toon_parser/
│   │   ├── __init__.py
│   │   ├── parser.py     # TOON → JSON parser
│   │   └── serializer.py # JSON → TOON serializer
│   ├── tests/
│   ├── pyproject.toml
│   └── setup.py
│
└── shared/                # Shared test fixtures
    └── test_cases.json   # Common test cases for both implementations
```

## Development Commands

### JavaScript/TypeScript

```bash
cd js/

# Install dependencies
npm install

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Build the package
npm run build

# Lint code
npm run lint

# Type check
npm run type-check

# Publish to npm
npm publish
```

### Python

```bash
cd python/

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

Both implementations must provide:

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

- **Shared test fixtures**: Use `shared/test_cases.json` for cross-language consistency
- **Round-trip tests**: Verify JSON → TOON → JSON produces identical results
- **Edge cases**: Empty arrays, null values, nested objects, special characters in strings
- **Token counting**: Benchmark token reduction vs JSON (target: 30-60% savings)
- **Accuracy tests**: If applicable, measure LLM parsing accuracy of generated TOON

## Reference Implementations

Existing TOON libraries (for reference, not dependencies):
- **TypeScript**: `@toon-format/toon` (official reference implementation)
- **Python**: Check npm/PyPI for community implementations
- **Spec**: https://github.com/toon-format/spec

## API Design

### JavaScript/TypeScript

```typescript
export function parse(toon: string): any;
export function stringify(json: any): string;
```

### Python

```python
def parse(toon: str) -> Any: ...
def stringify(json_obj: Any) -> str: ...
```

## Performance Considerations

- TOON is optimized for **uniform arrays** (e.g., logs, user lists, analytics events)
- For deeply nested non-uniform data, JSON may be more efficient
- Header definition has fixed cost; per-row savings compound with dataset size
- Quote handling is critical for performance (avoid regex where possible)
