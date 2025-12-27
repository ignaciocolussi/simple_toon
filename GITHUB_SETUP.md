# GitHub Repository Setup Guide

This guide walks through setting up the GitHub repository with CI/CD, automated testing, and publishing.

## 1. Initial Repository Setup

### Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `simple_toon`
3. Description: "Python parser and serializer for TOON (Token-Oriented Object Notation) - Reduce LLM token usage by 30-60%"
4. Choose: Public
5. **Do not** initialize with README (we already have one)
6. Click "Create repository"

### Push Code to GitHub
```bash
git remote add origin https://github.com/ignaciocolussi/simple_toon.git
git branch -M main
git push -u origin main
```

## 2. Branch Protection Rules

Protect the `main` branch to ensure code quality:

1. Go to **Settings** → **Branches** → **Add rule**
2. Branch name pattern: `main`
3. Enable these protections:
   - ✅ Require a pull request before merging
     - ✅ Require approvals: 1
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date before merging
     - Search and add these status checks (after first CI run):
       - `test (ubuntu-latest, 3.12)`
       - `test-examples`
       - `build`
   - ✅ Require conversation resolution before merging
   - ✅ Do not allow bypassing the above settings
4. Click **Create** or **Save changes**

## 3. GitHub Actions Secrets

### For PyPI Publishing

You need to configure PyPI trusted publishing (recommended) or use API tokens.

#### Option A: Trusted Publishing (Recommended - More Secure)

1. **On PyPI:**
   - Go to https://pypi.org/manage/account/publishing/
   - Click "Add a new publisher"
   - Fill in:
     - PyPI Project Name: `simple-toon`
     - Owner: `ignaciocolussi`
     - Repository name: `simple_toon`
     - Workflow name: `publish.yml`
     - Environment name: `pypi`
   - Click "Add"

2. **On TestPyPI (for testing):**
   - Go to https://test.pypi.org/manage/account/publishing/
   - Repeat the same process

#### Option B: API Tokens (Alternative)

1. **Get PyPI API Token:**
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Scope: Entire account (or specific to `simple-toon` after first publish)
   - Copy the token (starts with `pypi-`)

2. **Add to GitHub Secrets:**
   - Go to repository **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token
   - Click **Add secret**

3. **For TestPyPI:**
   - Get token from https://test.pypi.org/manage/account/token/
   - Add as secret: `TEST_PYPI_API_TOKEN`

### For Codecov (Optional - Code Coverage Reporting)

1. Go to https://codecov.io/ and sign in with GitHub
2. Add your repository
3. Get the upload token
4. Add to GitHub Secrets:
   - Name: `CODECOV_TOKEN`
   - Value: Your Codecov token

## 4. Environments Setup

For better security and deployment tracking:

1. Go to **Settings** → **Environments**
2. Click **New environment**

### Create `pypi` Environment:
- Name: `pypi`
- Protection rules:
  - ✅ Required reviewers: Add yourself or team members
  - Wait timer: 0 minutes (or add delay for safety)
- Environment secrets (if using API tokens):
  - `PYPI_API_TOKEN`: Your PyPI token

### Create `testpypi` Environment:
- Name: `testpypi`
- No protection rules needed
- Environment secrets (if using API tokens):
  - `TEST_PYPI_API_TOKEN`: Your TestPyPI token

## 5. Enable GitHub Actions

GitHub Actions should be enabled by default, but verify:

1. Go to **Settings** → **Actions** → **General**
2. Actions permissions: **Allow all actions and reusable workflows**
3. Workflow permissions: **Read and write permissions**
4. Click **Save**

## 6. Labels for Issues and PRs

Create labels for better organization:

1. Go to **Issues** → **Labels**
2. Add these labels:
   - `bug` (red) - Something isn't working
   - `enhancement` (blue) - New feature or request
   - `documentation` (green) - Documentation improvements
   - `good first issue` (purple) - Good for newcomers
   - `help wanted` (green) - Extra attention needed
   - `dependencies` (yellow) - Dependency updates
   - `python` (blue) - Python related
   - `github-actions` (purple) - CI/CD related
   - `performance` (orange) - Performance improvements
   - `breaking change` (red) - Breaking API changes

## 7. Repository Settings

### General Settings
1. **Settings** → **General**
   - Features:
     - ✅ Issues
     - ✅ Discussions (optional, for community Q&A)
     - ✅ Projects (if using GitHub Projects)
   - Pull Requests:
     - ✅ Allow squash merging
     - ✅ Allow merge commits
     - ✅ Allow rebase merging
     - ✅ Automatically delete head branches

### About Section
1. Click gear icon next to "About" on main repo page
2. Description: "Python parser and serializer for TOON (Token-Oriented Object Notation) - Reduce LLM token usage by 30-60%"
3. Website: Leave blank (or add docs site later)
4. Topics: `python`, `toon`, `json`, `parser`, `llm`, `token-optimization`, `data-format`
5. ✅ Include in the home page

## 8. First CI/CD Run

After pushing the GitHub Actions workflows:

```bash
git add .github/
git commit -m "ci: Add GitHub Actions workflows for testing and publishing"
git push
```

The tests will run automatically. Check:
- **Actions** tab to see workflow runs
- Fix any failures
- Green checkmarks = success!

## 9. Creating Your First Release

When ready to publish to PyPI:

1. **Update version** in `pyproject.toml` and `toon_parser/__init__.py`
2. **Update CHANGELOG.md** with changes
3. **Commit and push**:
   ```bash
   git add pyproject.toml toon_parser/__init__.py CHANGELOG.md
   git commit -m "chore: Bump version to 0.2.1"
   git push
   ```

4. **Create a git tag**:
   ```bash
   git tag v0.2.1
   git push origin v0.2.1
   ```

5. **Create GitHub Release**:
   - Go to **Releases** → **Draft a new release**
   - Choose tag: `v0.2.1`
   - Release title: `v0.2.1`
   - Description: Copy from CHANGELOG.md
   - Click **Publish release**

6. **Automatic Publishing**:
   - GitHub Actions will automatically build and publish to PyPI
   - Check **Actions** tab for progress
   - Verify on https://pypi.org/project/simple-toon/

## 10. Testing the Publish Workflow

Before publishing to production PyPI, test on TestPyPI:

1. Go to **Actions** tab
2. Click **Publish to PyPI** workflow
3. Click **Run workflow**
4. Check ✅ "Publish to TestPyPI instead of PyPI"
5. Click **Run workflow**
6. Verify on https://test.pypi.org/project/simple-toon/

## 11. Monitoring and Maintenance

### Regular Checks
- Monitor **Actions** tab for CI failures
- Review **Dependabot** PRs weekly
- Respond to **Issues** and **Pull Requests** promptly
- Keep **CHANGELOG.md** updated

### Badges (Optional)
Add to README.md:

```markdown
[![Tests](https://github.com/ignaciocolussi/simple_toon/workflows/Tests/badge.svg)](https://github.com/ignaciocolussi/simple_toon/actions)
[![PyPI version](https://badge.fury.io/py/simple-toon.svg)](https://pypi.org/project/simple-toon/)
[![Python versions](https://img.shields.io/pypi/pyversions/simple-toon.svg)](https://pypi.org/project/simple-toon/)
[![codecov](https://codecov.io/gh/ignaciocolussi/simple_toon/branch/main/graph/badge.svg)](https://codecov.io/gh/ignaciocolussi/simple_toon)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

## Troubleshooting

### CI Fails on First Run
- Check the **Actions** tab for error details
- Common issues:
  - Missing dependencies in `pyproject.toml`
  - Python version incompatibilities
  - Test failures

### Publishing Fails
- Verify GitHub Secrets are set correctly
- Check environment configuration
- Ensure PyPI trusted publishing is configured
- Verify version number is unique (can't republish same version)

### Pre-commit Hooks Fail
- Install pre-commit: `pip install pre-commit`
- Install hooks: `pre-commit install`
- Run manually: `pre-commit run --all-files`
- Fix any issues reported

## Summary

You now have:
- ✅ Automated testing on every push/PR
- ✅ Multi-version Python testing (3.8-3.12)
- ✅ Automatic PyPI publishing on releases
- ✅ Code quality checks (black, ruff, mypy)
- ✅ Pre-commit hooks for local development
- ✅ Issue and PR templates
- ✅ Dependabot for dependency updates
- ✅ Branch protection for code quality
- ✅ Professional CI/CD pipeline

Your repository is now production-ready! 🚀
