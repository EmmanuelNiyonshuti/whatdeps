# whatdeps
[![Tests](https://github.com/EmmanuelNiyonshuti/whatdeps/actions/workflows/ci.yml/badge.svg)](https://github.com/EmmanuelNiyonshuti/whatdeps/actions)
[![codecov](https://codecov.io/gh/EmmanuelNiyonshuti/whatdeps/graph/badge.svg?token=6HA3SJLM0F)](https://codecov.io/gh/EmmanuelNiyonshuti/whatdeps)
[![PyPI](https://img.shields.io/pypi/v/whatdeps.svg)](https://pypi.org/project/whatdeps/)
[![Python](https://img.shields.io/pypi/pyversions/whatdeps.svg)](https://pypi.org/project/whatdeps/)
[![](https://img.shields.io/github/license/EmmanuelNiyonshuti/whatdeps.svg)](https://github.com/EmmanuelNiyonshuti/whatdeps/blob/master/LICENSE.md)
![t](https://img.shields.io/badge/status-maintained-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-github%20pages-blue)](https://EmmanuelNiyonshuti.github.io/whatdeps/)

A tiny CLI tool that shows basic information about a Python project’s dependencies using  few pieces of information from PyPI and GitHub.

## it shows

- **Supported Python versions** - minimum version required
- **Disk size** - space it takes up
- **Last release** - when it was last updated on PyPI
- **Last push** - recent activity on GitHub
- **Issues** - open/closed ratio (to give a sense of maintenance)
- **Stars** - popularity on GitHub

## Installation

You can install it from [PyPI](https://pypi.org/project/whatdeps/)
```bash
# With uv
uv tool install whatdeps

# or pipx
pipx install whatdeps
```
or
You can install it in your project environment(not recommended!)
```bash
# With pip
pip install whatdeps

# Or uv
uv add whatdeps
```

## Usage

Run it in any Python project with a dependency specification file:
```bash
whatdeps
```
Or point it at a specific file:
```bash
whatdeps -f requirements.txt
whatdeps -f pyproject.toml
```

## Example output
```
 Inspecting 4 packages (4 prod, 0 dev)
  Fetching metadata from PyPI and GitHub... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

                                     Production Dependencies
╭──────────────┬──────────────┬──────────┬───────────────┬──────────────┬──────────────┬─────────╮
│              │  Supported   │  Size on │ Last Release  │  Last Push   │ Issues (O/C) │  Stars  │
│ Package      │    Python    │   Disk   │   on PyPI     │  on GitHub   │  on GitHub   │         │
├──────────────┼──────────────┼──────────┼───────────────┼──────────────┼──────────────┼─────────┤
│ authlib      │    >=3.9     │   1.3MB  │  2024-12-12   │  2025-01-21  │   130/414    │  5,184  │
│ fastapi      │    >=3.9     │   1.3MB  │  2024-12-27   │  2025-01-23  │  212/3471    │ 94,390  │
│ pwdlib       │    >=3.10    │  32.2KB  │  2024-10-25   │  2024-12-11  │    2/10      │   126   │
│ pytest       │    >=3.10    │  25.2KB  │  2024-12-06   │  2025-01-19  │  980/5373    │ 13,483  │
├──────────────┼──────────────┼──────────┼───────────────┼──────────────┼──────────────┼─────────┤
│              │     Total    │          │     2.7MB     │              │              │         │
╰──────────────┴──────────────┴──────────┴───────────────┴──────────────┴──────────────┴─────────╯

╭─────────────────────────────────── Summary ───────────────────────────────────╮
│ Total Packages: 4                                                             │
│ Total Disk Usage: 2.7MB                                                       │
│                                                                               │
│ Issues shown as Open/Closed ratio                                            │
╰───────────────────────────────────────────────────────────────────────────────╯
```

## Supported formats

- `pyproject.toml` ([PEP 621](https://peps.python.org/pep-0621/), Poetry, Hatch)
- `requirements.txt` and other common formats (`requirements-dev.txt`, etc.)
Dependencies are parsed according to [PEP 508](https://peps.python.org/pep-0508/). Development dependencies follow [PEP 735](https://peps.python.org/pep-0735/) groupings.

Packages in `requirements.txt` are treated as production dependencies; those from other pip requirements files are considered as other dependencies.

## Local development
 
this project uses [tox](https://tox.wiki/en/4.17.2/installation.html) for testing and documentation building, [sphinx](https://www.sphinx-doc.org/en/master/) for docs, and [pytest](https://docs.pytest.org/en/stable/) for tests.
 
build the docs:
```bash
tox -e docs
```
output goes to `docs/_build`.
 
run tests on a specific Python version:
```bash
tox -e py3.x -- tests
```
run tests across all environments in parallel:
```bash
tox -p -- tests
```
you can also use `uv` to create a virtual environment and sync dependencies:
```bash
uv sync
```

## LICENCE
MIT. See the `LICENSE` file for details.