# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added
- Initial release of n8n-nodes-toon
- Parse operation: Convert TOON format to JSON
- Stringify operation: Convert JSON to TOON format
- Validate operation: Check TOON format validity
- Auto-detect and convert operation: Smart bidirectional conversion
- Support for input from fields or direct parameters
- Comprehensive error handling with clear error messages
- Full TypeScript implementation ported from Python toon_parser

### Features
- Lossless conversion between JSON and TOON
- Type inference for numbers, booleans, and null values
- Proper quote escaping for strings with special characters
- Support for uniform arrays with tabular layout
- 30-60% token reduction for LLM workflows
