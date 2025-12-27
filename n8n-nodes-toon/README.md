# n8n-nodes-simple-toon

This is an n8n community node for working with **TOON (Token-Oriented Object Notation)** - a compact data format designed to reduce LLM token consumption by 30-60% compared to JSON while maintaining lossless conversion.

[n8n](https://n8n.io/) is a [fair-code licensed](https://docs.n8n.io/reference/license/) workflow automation platform.

## Features

- **Parse (TOON → JSON)**: Convert TOON format strings to JSON objects
- **Stringify (JSON → TOON)**: Convert JSON objects to TOON format strings
- **Validate**: Check if a string is valid TOON format
- **Auto-Detect and Convert**: Automatically detect format and convert bidirectionally

## Installation

Follow the [installation guide](https://docs.n8n.io/integrations/community-nodes/installation/) in the n8n community nodes documentation.

### Community Node Installation

1. Go to **Settings** > **Community Nodes**
2. Select **Install**
3. Enter `n8n-nodes-simple-toon` in **Enter npm package name**
4. Agree to the [risks](https://docs.n8n.io/integrations/community-nodes/risks/) of using community nodes
5. Select **Install**

After installation the TOON node will be available in your n8n instance.

## Operations

### Parse (TOON → JSON)

Converts TOON format strings to JSON objects.

**Input:**
```
users[2]{id,name,active}:
  1,Alice,true
  2,Bob,false
```

**Output:**
```json
{
  "users": [
    {"id": 1, "name": "Alice", "active": true},
    {"id": 2, "name": "Bob", "active": false}
  ]
}
```

### Stringify (JSON → TOON)

Converts JSON objects to TOON format strings.

**Input:**
```json
{
  "users": [
    {"id": 1, "name": "Alice", "active": true}
  ]
}
```

**Output:**
```
users[1]{id,name,active}:
  1,Alice,true
```

### Validate

Checks if a string is valid TOON format.

**Output:**
```json
{
  "valid": true,
  "format": "toon",
  "error": null
}
```

### Auto-Detect and Convert

Automatically detects whether the input is TOON or JSON and converts it to the opposite format.

**Output:**
```json
{
  "output": "...",
  "detectedFormat": "toon",
  "convertedFrom": "toon",
  "convertedTo": "json"
}
```

## Usage Examples

### Example 1: Convert API Response to TOON for LLM Processing

1. **HTTP Request** node fetches user data from API (JSON)
2. **TOON** node (Stringify operation) converts to TOON format
3. **OpenAI** node processes the compact TOON data (saves tokens!)
4. **TOON** node (Parse operation) converts result back to JSON

### Example 2: Validate TOON Data Before Processing

1. **Webhook** node receives TOON data
2. **TOON** node (Validate operation) checks format
3. **IF** node branches based on validation result
4. **TOON** node (Parse operation) processes valid data

### Example 3: Smart Format Conversion

1. **Code** node or webhook receives data in unknown format
2. **TOON** node (Auto-Detect and Convert) automatically handles conversion
3. Continue workflow with converted data

## TOON Format Overview

TOON is optimized for uniform arrays of objects (tabular/semi-structured data):

### Syntax
```
arrayName[count]{field1,field2,field3}:
  value1,value2,value3
  value1,value2,value3
```

### Key Features
- **Compact**: 30-60% fewer tokens than JSON
- **Lossless**: Perfect round-trip conversion (JSON ↔ TOON)
- **Type-aware**: Automatically infers numbers, booleans, null
- **Readable**: YAML-style indentation + CSV-style data rows

### Best For
- User lists, analytics events, logs
- Tabular data with uniform structure
- LLM-based workflows where token count matters

### Not Ideal For
- Deeply nested non-uniform data
- Small objects (JSON may be more efficient)

## Compatibility

- **n8n version**: 0.187.0 or later
- **Node.js version**: 14.0.0 or later

## Resources

- [n8n community nodes documentation](https://docs.n8n.io/integrations/community-nodes/)
- [TOON Python Package](https://pypi.org/project/toon-parser/)
- [TOON Specification](https://github.com/toon-format/spec)

## Development

### Building the Node

```bash
npm install
npm run build
```

### Testing Locally

```bash
# Link the package
npm link

# In your n8n installation
cd ~/.n8n/nodes
npm link n8n-nodes-toon

# Restart n8n
```

### Linting and Formatting

```bash
npm run lint
npm run format
```

## License

[MIT](LICENSE.md)

## Version History

### 0.1.0 (Initial Release)
- Parse TOON to JSON
- Stringify JSON to TOON
- Validate TOON format
- Auto-detect and convert

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/ignaciocolussi/toon_parser).
