# Development Guide

This guide covers development, testing, and publishing of the n8n-nodes-toon community node.

## Prerequisites

- Node.js 14.0.0 or later
- npm 6.0.0 or later
- n8n installed (for testing)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/ignaciocolussi/toon_parser.git
cd toon_parser/n8n-nodes-toon
```

2. Install dependencies:
```bash
npm install
```

## Project Structure

```
n8n-nodes-toon/
├── nodes/
│   └── Toon/
│       ├── Toon.node.ts          # Main node implementation
│       ├── ToonParser.ts          # TOON → JSON parser
│       ├── ToonSerializer.ts      # JSON → TOON serializer
│       ├── ToonUtils.ts           # Validation and utilities
│       └── toon.svg               # Node icon
├── credentials/                   # (Empty - no credentials needed)
├── examples/
│   └── example-workflow.json      # Example n8n workflow
├── dist/                          # Build output (generated)
├── package.json                   # Package metadata
├── tsconfig.json                  # TypeScript configuration
├── gulpfile.js                    # Build tasks
├── .eslintrc.js                   # Linting rules
└── README.md                      # User documentation
```

## Development Workflow

### 1. Build the Node

Compile TypeScript and copy assets:

```bash
npm run build
```

This will:
- Compile TypeScript files to JavaScript
- Copy icon files to `dist/`
- Generate type definitions

### 2. Link for Local Testing

Link the package to test in your local n8n:

```bash
# In the n8n-nodes-toon directory
npm link

# In your n8n custom nodes directory (usually ~/.n8n/nodes)
cd ~/.n8n/nodes
npm link n8n-nodes-toon
```

Alternatively, for n8n Desktop or Docker:

```bash
# Copy to n8n custom nodes
cp -r dist/* ~/.n8n/nodes/
```

### 3. Restart n8n

After linking or copying, restart n8n to load the node:

```bash
n8n start
```

The TOON node should now appear in the nodes panel under "Transform" category.

## Development Commands

### Build

```bash
npm run build          # Full build (TypeScript + icons)
npm run dev            # Watch mode for development
```

### Linting and Formatting

```bash
npm run lint           # Check code style
npm run lintfix        # Auto-fix linting issues
npm run format         # Format code with Prettier
```

### Pre-publish Checks

```bash
npm run prepublishOnly # Run before publishing to npm
```

## Testing

### Manual Testing

1. Build and link the node (see above)
2. Open n8n in your browser
3. Create a new workflow
4. Add the TOON node
5. Test each operation:
   - **Parse**: Input TOON, verify JSON output
   - **Stringify**: Input JSON, verify TOON output
   - **Validate**: Test with valid/invalid TOON
   - **Auto-Convert**: Test with both JSON and TOON inputs

### Test Cases

Import `examples/example-workflow.json` into n8n for quick testing.

#### Parse Operation Test
```
Input (TOON):
users[2]{id,name,active}:
  1,Alice,true
  2,Bob,false

Expected Output:
{"users": [{"id": 1, "name": "Alice", "active": true}, {"id": 2, "name": "Bob", "active": false}]}
```

#### Stringify Operation Test
```
Input (JSON):
{"products": [{"id": 1, "name": "Widget", "price": 9.99}]}

Expected Output:
products[1]{id,name,price}:
  1,Widget,9.99
```

#### Validate Operation Test
```
Input (valid TOON):
items[1]{id}:
  1

Expected Output:
{"valid": true, "format": "toon", "error": null}
```

## Code Organization

### ToonParser.ts

Implements TOON parsing logic:
- `parse()`: Main parsing function
- `parseLines()`: Line-by-line parser
- `parseRow()`: CSV-style row parser with quote handling
- `parseValue()`: Type inference for primitives

### ToonSerializer.ts

Implements TOON serialization:
- `stringify()`: Main serialization function
- `stringifyDict()`: Object serialization
- `isUniformArray()`: Array uniformity detection
- `quoteIfNeeded()`: Smart string quoting

### ToonUtils.ts

Utility functions:
- `validate()`: Format validation
- `detectFormat()`: Auto-detection (TOON vs JSON)
- `autoConvert()`: Bidirectional conversion

### Toon.node.ts

n8n node implementation:
- Node descriptor (UI configuration)
- Operation handlers
- Input/output processing
- Error handling

## Publishing to npm

### 1. Pre-publish Checklist

- [ ] All tests pass
- [ ] Code is linted (`npm run lint`)
- [ ] Version bumped in `package.json`
- [ ] CHANGELOG.md updated
- [ ] README.md reviewed
- [ ] Build succeeds (`npm run build`)

### 2. Build and Test

```bash
npm run build
npm run prepublishOnly
```

### 3. Publish

```bash
npm login
npm publish
```

### 4. Verify Publication

Check that the package appears at:
- https://www.npmjs.com/package/n8n-nodes-toon
- https://n8n.io/integrations (community nodes)

## Version Management

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes to node API
- **MINOR**: New operations or backward-compatible features
- **PATCH**: Bug fixes

Update version in:
1. `package.json`
2. `CHANGELOG.md`

## Troubleshooting

### Node Not Appearing in n8n

1. Check n8n logs for errors
2. Verify `package.json` has correct `n8n.nodes` configuration
3. Ensure build succeeded and `dist/` contains compiled files
4. Restart n8n completely

### TypeScript Compilation Errors

```bash
# Clean build
rm -rf dist/
npm run build
```

### Linting Issues

```bash
npm run lintfix  # Auto-fix
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Resources

- [n8n Node Development Docs](https://docs.n8n.io/integrations/creating-nodes/)
- [n8n Community Nodes](https://docs.n8n.io/integrations/community-nodes/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## Support

For bugs or feature requests, open an issue at:
https://github.com/ignaciocolussi/toon_parser/issues
