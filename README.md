# whatdeps

<!-- [![Tests](https://github.com/EmmanuelNiyonshuti/whatdeps/actions/workflows/tests.yml/badge.svg)](https://github.com/EmmanuelNiyonshuti/whatdeps/actions) -->
[![codecov](https://codecov.io/gh/EmmanuelNiyonshuti/whatdeps/graph/badge.svg?token=6HA3SJLM0F)](https://codecov.io/gh/EmmanuelNiyonshuti/whatdeps)
[![PyPI](https://img.shields.io/pypi/v/whatdeps.svg)](https://pypi.org/project/whatdeps/)
[![Python](https://img.shields.io/pypi/pyversions/whatdeps.svg)](https://pypi.org/project/whatdeps/)

A small cli tool that shows you informations with your Python dependencies. it checks PyPI for release info and GitHub for activity.

## Install
```bash
pip install whatdeps
```

## Usage

Run it in any Python project:
```bash
whatdeps
```

Or point it at a specific file:
```bash
whatdeps -f requirements.txt
whatdeps -f pyproject.toml
```

## What it shows

- **Supported Python versions** - minimum version required
- **Disk size** - space it takes up (if installed)
- **Last release** - when it was last updated on PyPI
- **Last push** - recent activity on GitHub
- **Issues** - open/closed ratio (gives you a sense of maintenance)
- **Stars** - popularity on GitHub

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

- `pyproject.toml` (PEP 621, Poetry, Hatch)
- `requirements.txt`
- `requirements-dev.txt`
- Other common requirements file patterns

## Development
```bash
git clone https://github.com/EmmanuelNiyonshuti/whatdeps.git
cd whatdeps
pip install -e ".[dev]"
pytest
```


## License

MIT