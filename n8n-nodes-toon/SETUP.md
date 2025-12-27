# Quick Setup Guide

Get your n8n-nodes-toon package up and running in minutes.

## Installation

### Option 1: Install from npm (Recommended)

Once published to npm:

```bash
# In n8n, go to Settings > Community Nodes
# Enter: n8n-nodes-simple-toon
```

### Option 2: Install Locally for Development

```bash
cd /home/ignac/toon_parser/n8n-nodes-toon

# Install dependencies
npm install

# Build the node
npm run build

# Link for testing
npm link

# In your n8n installation
cd ~/.n8n/custom
npm link n8n-nodes-simple-toon

# Restart n8n
```

## First Time Build

```bash
# From the n8n-nodes-toon directory
npm install
npm run build
```

This will create the `dist/` folder with compiled JavaScript and assets.

## Publishing to npm

Before first publish:

1. Update your author email in `package.json`:
```json
"author": {
  "name": "Ignacio Colussi",
  "email": "your-actual-email@example.com"
}
```

2. Verify repository URLs match your GitHub repo

3. Build and publish:
```bash
npm run build
npm login
npm publish
```

## Testing in n8n

1. Start n8n:
```bash
n8n start
```

2. Open n8n in browser (usually http://localhost:5678)

3. Create new workflow

4. Search for "TOON" in nodes panel

5. Add the TOON node and test operations

## Quick Test

Try this TOON input with the **Parse** operation:

```
users[3]{id,name,email}:
  1,Alice,alice@example.com
  2,Bob,bob@example.com
  3,Charlie,charlie@example.com
```

You should get:

```json
{
  "users": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
  ]
}
```

## Project Files Overview

```
n8n-nodes-toon/
├── nodes/Toon/              # Node implementation
│   ├── Toon.node.ts         # Main node file
│   ├── ToonParser.ts        # Parser (TOON → JSON)
│   ├── ToonSerializer.ts    # Serializer (JSON → TOON)
│   ├── ToonUtils.ts         # Utilities
│   └── toon.svg             # Node icon
├── package.json             # npm package config
├── tsconfig.json            # TypeScript config
├── gulpfile.js              # Build tasks
├── README.md                # User docs
├── DEVELOPMENT.md           # Developer guide
└── SETUP.md                 # This file
```

## Troubleshooting

### "TOON node not found"

- Ensure build succeeded: `npm run build`
- Check `dist/` folder exists
- Restart n8n completely
- Check n8n logs for errors

### TypeScript errors

```bash
rm -rf dist/ node_modules/
npm install
npm run build
```

### Icon not showing

Icons are copied during build:
```bash
npm run build
# Check dist/nodes/Toon/toon.svg exists
```

## Next Steps

- Read [README.md](README.md) for usage examples
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for detailed dev guide
- Import [examples/example-workflow.json](examples/example-workflow.json) into n8n
- Publish to npm to share with community

## Support

Questions or issues? Open an issue at:
https://github.com/ignaciocolussi/simple_toon/issues
