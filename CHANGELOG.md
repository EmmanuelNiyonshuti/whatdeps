# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.1] - 2026-03-12

### Added
- Added `--version` option for showing `whatdeps` version
- CI publishing via GitHub Actions. no more manual `python3 -m build && twine upload dist/*`.

### Changed
- Removed `__main__.py` entry point.
- Added `run()` function as what the cli calls with the passed in arguments. the function lives inside `utils.py` and it is into three phases: `_scan_dependencies`, `_print_summary`, and `_inspect_packages`.
- `run()` is now a plain sync function. `asyncio.run()` is scoped only to `_inspect_packages`, The one truly async operation (network I/O). File reading stays blocking with the builtin `open()`.

- Updated `progress` spinner to disappear after showcasing fetching metadata from pypi/github.

## [0.1.0.post2] - 2026-02-26

### Changed
- Renamed `async_main`.
- Added type hints.
- Improved README.

### Fixed
- Test warning: coroutine was never awaited.
- Typos in README.
- Packaging metadata.

## [0.1.0.post1] - 2026-01-24

### Changed
- Added `tox` for testing across multiple Python environments.
- Improved README added `pipx` and `uv` installation options.

## [0.1.0] - 2026-01-23

### Added
- Initial release.
- `whatdeps` CLI command to inspect Python dependencies from PyPI and GitHub.
- Support for `pyproject.toml` and `requirements.txt`.
- Rich terminal display with spinner and progress bar.

[Unreleased]: https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.0.post2...v0.1.1
[0.1.0.post2]: https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.0.post1...v0.1.0.post2
[0.1.0.post1]: https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.0...v0.1.0.post1
[0.1.0]: https://github.com/EmmanuelNiyonshuti/whatdeps/releases/tag/v0.1.0