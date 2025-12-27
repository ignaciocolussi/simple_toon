# Publishing to PyPI

This guide explains how to build and publish the `simple-toon` package to PyPI.

## Prerequisites

1. **PyPI Account**
   - Create account at https://pypi.org/account/register/
   - Create account at https://test.pypi.org/account/register/ (for testing)

2. **API Tokens** (recommended over passwords)
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - Save tokens securely (they won't be shown again)

3. **Install build tools**
   ```bash
   pip install build twine
   # OR install with dev dependencies
   pip install -e ".[dev]"
   ```

## Step-by-Step Publishing

### 1. Pre-flight Checks

```bash
# Ensure you're in the python directory
cd python

# Run all tests
pytest

# Check code quality
black toon_parser/ tests/ --check
ruff check toon_parser/ tests/
mypy toon_parser/

# Verify version number in pyproject.toml matches toon_parser/__init__.py
grep "version =" pyproject.toml
grep "__version__" toon_parser/__init__.py
```

### 2. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ *.egg-info
```

### 3. Build the Package

```bash
# Build source distribution and wheel
python -m build

# This creates:
# - dist/simple_toon-0.2.0.tar.gz (source distribution)
# - dist/simple_toon-0.2.0-py3-none-any.whl (wheel)
```

### 4. Check the Distribution

```bash
# Verify the package is well-formed
twine check dist/*

# Should output: "Checking dist/... PASSED"
```

### 5. Upload to TestPyPI (RECOMMENDED FIRST)

```bash
# Upload to TestPyPI to verify everything works
twine upload --repository testpypi dist/*

# You'll be prompted for username and password/token:
# Username: __token__
# Password: pypi-... (your TestPyPI API token)
```

### 6. Test Installation from TestPyPI

```bash
# Create a fresh virtual environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ simple-toon

# Test the package
python -c "from toon_parser import parse, stringify; print('✓ Import successful')"

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

### 7. Upload to PyPI (PRODUCTION)

```bash
# If TestPyPI worked, upload to real PyPI
twine upload dist/*

# You'll be prompted for username and password/token:
# Username: __token__
# Password: pypi-... (your PyPI API token)
```

### 8. Verify on PyPI

Visit https://pypi.org/project/simple-toon/ to see your package!

### 9. Test Installation from PyPI

```bash
# Create a fresh virtual environment
python -m venv verify_env
source verify_env/bin/activate

# Install from PyPI
pip install simple-toon

# Test
python -c "from toon_parser import parse, stringify, ToonParser; print('✓ Success')"

deactivate
rm -rf verify_env
```

## Using API Tokens (Recommended)

### Configure .pypirc

Create `~/.pypirc` with your API tokens:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

Set permissions:
```bash
chmod 600 ~/.pypirc
```

Now you can upload without entering credentials:
```bash
twine upload dist/*
```

## Automation with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install build twine

    - name: Build package
      run: python -m build
      working-directory: python

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload python/dist/*
```

Add your PyPI token as a GitHub secret named `PYPI_API_TOKEN`.

## Version Bump Checklist

Before each release:

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `toon_parser/__init__.py`
- [ ] Update `CHANGELOG.md` with new version
- [ ] Run full test suite: `pytest`
- [ ] Check code quality: `black`, `ruff`, `mypy`
- [ ] Update `README.md` if needed
- [ ] Commit changes: `git commit -am "Bump version to X.Y.Z"`
- [ ] Create git tag: `git tag vX.Y.Z`
- [ ] Push with tags: `git push && git push --tags`
- [ ] Build and test on TestPyPI
- [ ] Upload to PyPI
- [ ] Create GitHub release with changelog

## Troubleshooting

### "File already exists"
- You can't overwrite published versions
- Bump the version number in `pyproject.toml` and rebuild

### "Invalid distribution"
- Run `twine check dist/*` to see specific errors
- Ensure `README.md` is valid Markdown
- Check that `LICENSE` file exists

### "Authentication failed"
- Verify your API token is correct
- Ensure username is `__token__` (not your PyPI username)
- Check token hasn't expired

### Import errors after install
- Ensure `__init__.py` exports are correct
- Check `pyproject.toml` package discovery settings
- Verify MANIFEST.in includes necessary files

## Quick Reference

```bash
# Full workflow
rm -rf dist/ && \
python -m build && \
twine check dist/* && \
twine upload --repository testpypi dist/* && \
# Test on TestPyPI, then:
twine upload dist/*
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
