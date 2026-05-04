Usage
=====

Basic usage
-----------

Run ``whatdeps`` from the root of any Python project. It will automatically look for
a supported dependency file in the current directory::

   whatdeps

Specifying a file
-----------------

You can also point ``whatdeps`` at a specific file using the ``-f`` / ``--file`` flag::

   whatdeps -f requirements.txt
   whatdeps -f pyproject.toml

Command-line reference
----------------------

.. code-block:: text

   usage: whatdeps [-h] [-f FILE] [-v]

   Get to know about your Python project dependency informations from PyPi and GitHub

   options:
     -h, --help            show this help message and exit
     -f FILE, --file FILE  Path to pyproject.toml or requirements.txt
                           (will auto-detect if not specified)
     -v, --version         show program's version number and exit

Supported dependency file formats
-----------------------------------

``whatdeps`` can parse the following file formats:

``pyproject.toml``
   Supports `PEP 621 <https://peps.python.org/pep-0621/>`_ (standard ``[project]``
   table), `Poetry <https://python-poetry.org/>`_ (``[tool.poetry]``), and
   `Hatch <https://hatch.pypa.io/>`_ (``[tool.hatch.envs.*]``).
   Development dependencies are detected from ``[dependency-groups]``
   (`PEP 735 <https://peps.python.org/pep-0735/>`_), Poetry groups, and Hatch envs.

``requirements.txt``
   Packages are treated as **production** dependencies.

``requirements-dev.txt`` and other pip requirements files
   Packages from files other than ``requirements.txt`` are treated as
   **other** (development) dependencies.

Auto-detection order
~~~~~~~~~~~~~~~~~~~~~

When no ``-f`` flag is given, ``whatdeps`` checks the current directory in this order:

1. ``pyproject.toml``
2. ``requirements.txt``
3. ``requirements-dev.txt``
4. Other known requirements files

If none are found, ``whatdeps`` exits with an error.

Understanding the output
-------------------------

``whatdeps`` renders a Rich table in your terminal with one row per dependency.
Columns are colour-coded based on recency to give a quick sense of how actively
each package is maintained.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Column
     - Description
   * - **Package**
     - The package name as it appears on PyPI.
   * - **Supported Python**
     - The ``python_requires`` specifier from PyPI (e.g. ``>=3.9``).
   * - **Size on Disk**
     - Approximate compressed size of the wheel/sdist on PyPI.
   * - **Last Release on PyPI**
     - Date of the most recent release. Green < 30 days, yellow < 180 days, grey older.
   * - **Last Push on GitHub**
     - Date of the most recent push. Green < 90 days, yellow < 365 days, red older.
   * - **Issues (O/C)**
     - Open / closed issue count. Green when >80 % closed, yellow >60 %, red otherwise.
   * - **Stars**
     - GitHub star count. Bold when > 1 000.

A **Summary** panel at the bottom shows total package count and total disk usage.

Example output
--------------

.. code-block:: text

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

Exit codes
----------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Meaning
   * - ``0``
     - Success.
   * - ``1``
     - An error occurred (file not found, parsing error, or unexpected failure).
   * - ``130``
     - Interrupted by the user (``Ctrl+C``).