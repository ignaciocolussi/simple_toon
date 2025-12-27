# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-27

### Added
- **Streaming Serializer** for memory-efficient writing of large TOON files
  - `StreamingSerializer` class for streaming writes
  - `streaming_serializer()` context manager
  - `stream_from_database()` helper for database exports
  - Write 10,000+ items with constant memory usage

- **Object-Oriented API** as alternative to functional API
  - `ToonParser` class for stateful parsing with configuration
  - `ToonSerializer` class for stateful serialization
  - `ToonDocument` class for document object model with query/manipulation
  - `ToonConverter` class for format conversion with statistics

- **Schema Validation System**
  - `Schema` and `Field` classes for defining validation rules
  - `MultiSchema` for validating multiple arrays
  - `infer_schema()` for automatic schema generation
  - Support for field types, constraints, patterns, enums, and custom validators

- **File I/O Utilities**
  - `read_toon()` and `write_toon()` with optional schema validation
  - `convert_json_to_toon()` and `convert_toon_to_json()`
  - `batch_convert()` for directory-level conversion
  - `get_file_stats()` for file analysis

- **Advanced Features**
  - Nested object support with automatic flattening/unflattening
  - Multiple root arrays in single document
  - Streaming parser for memory-efficient reading
  - Configurable separators and indentation
  - Quoted string preservation for type safety

### Changed
- Updated to Python 3.8+ (was unspecified)
- Improved error messages with better context
- Enhanced type hints throughout codebase

### Fixed
- Quote-aware parsing to preserve string types vs numbers
- Multiple array parsing in single document
- Indentation handling for nested structures

## [0.1.0] - 2025-12-27

### Added
- Initial release
- Basic TOON parsing and serialization
- Support for uniform arrays
- Type inference (int, float, bool, string, null)
- Round-trip conversion (JSON ↔ TOON)
- Basic error handling

[0.2.0]: https://github.com/ignac/simple-toon/releases/tag/v0.2.0
[0.1.0]: https://github.com/ignac/simple-toon/releases/tag/v0.1.0
