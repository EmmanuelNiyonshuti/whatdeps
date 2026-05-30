Changelog
=========

All notable changes to this project will be documented in this file.

Unreleased
----------

`Compare unreleased changes <https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.2...HEAD>`_

0.1.2 - 2026-05-30
------------------

Changed
~~~~~~~

- Improved type annotations across the codebase.
- Added Sphinx documentation.

`Full diff <https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.1...v0.1.2>`_

0.1.1 — 2026-03-12
-------------------

Added
~~~~~

- ``--version`` flag to display the current ``whatdeps`` version.
- CI publishing via GitHub Actions — no more manual ``python3 -m build && twine upload dist/*``.

Changed
~~~~~~~

- Removed ``__main__.py`` entry point.
- Added ``run()`` function as the entry point called by the CLI with parsed arguments.
  The function lives in ``utils.py`` and is split into three phases:
  ``_scan_dependencies``, ``_print_summary``, and ``_inspect_packages``.
- ``run()`` is now a plain synchronous function. ``asyncio.run()`` is scoped only to
  ``_inspect_packages`` — the one truly async operation (network I/O). File reading
  stays blocking with the built-in ``open()``.
- Updated progress spinner to disappear after displaying the fetched metadata.

`Full diff <https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.0.post2...v0.1.1>`_

0.1.0.post2 — 2026-02-26
-------------------------

Changed
~~~~~~~

- Renamed ``async_main``.
- Improved README.

Fixed
~~~~~

- Test warning: coroutine was never awaited.
- Typos in README.
- Packaging metadata corrections.

`Full diff <https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.0.post1...v0.1.0.post2>`_

0.1.0.post1 — 2026-01-24
-------------------------

Changed
~~~~~~~

- Added ``tox`` for testing across multiple Python environments.
- Improved README with ``pipx`` and ``uv`` installation options.

`Full diff <https://github.com/EmmanuelNiyonshuti/whatdeps/compare/v0.1.0...v0.1.0.post1>`_

0.1.0 — 2026-01-23
-------------------

Added
~~~~~

- Initial release.
- ``whatdeps`` CLI command to inspect Python dependencies from PyPI and GitHub.
- Support for ``pyproject.toml`` and ``requirements.txt``.
- Rich terminal display with spinner and progress bar.

`Full diff <https://github.com/EmmanuelNiyonshuti/whatdeps/releases/tag/v0.1.0>`_
