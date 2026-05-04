whatdeps
========

.. toctree::
   :maxdepth: 2
   :hidden:

   installation
   usage
   changelog

A tiny CLI tool that shows basic information about a Python project's dependencies
using a few pieces of information from PyPI and GitHub.

Given a dependency file (``pyproject.toml`` or ``requirements.txt``), ``whatdeps``
fetches metadata from PyPI and GitHub and renders a summary table directly in your
terminal — no configuration required.

.. code-block:: text

    Inspecting 4 packages (4 prod, 0 dev)
    Fetching metadata from PyPI and GitHub... ━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

                             Production Dependencies
   ╭──────────────┬──────────────┬──────────┬──────────────┬──────────────╮
   │ Package      │  Supported   │  Size on │ Last Release │  Last Push   │
   │              │    Python    │   Disk   │   on PyPI    │  on GitHub   │
   ├──────────────┼──────────────┼──────────┼──────────────┼──────────────┤
   │ fastapi      │    >=3.9     │   1.3MB  │  2024-12-27  │  2025-01-23  │
   │ pytest       │    >=3.10    │  25.2KB  │  2024-12-06  │  2025-01-19  │
   ╰──────────────┴──────────────┴──────────┴──────────────┴──────────────╯