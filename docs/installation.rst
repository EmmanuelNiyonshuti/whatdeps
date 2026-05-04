Installation
============

Requirements
------------

``whatdeps`` requires **Python 3.11 or newer**.

As a standalone CLI tool
------------------------

The recommended way to install ``whatdeps`` is as an isolated command-line tool
using ``uv tool`` or ``pipx``. This keeps it out of your project's virtual environment.

With ``uv``::

   uv tool install whatdeps

With ``pipx``::

   pipx install whatdeps

After installation, the ``whatdeps`` command will be available globally in your shell.

Inside a project environment
-----------------------------

You can also install ``whatdeps`` as a regular package dependency if you want to pin
it alongside your project tooling.

With ``pip``::

   pip install whatdeps

With ``uv``::

   uv add whatdeps

Verifying the installation
---------------------------

Run the following to confirm ``whatdeps`` is installed and check the version::

   whatdeps --version