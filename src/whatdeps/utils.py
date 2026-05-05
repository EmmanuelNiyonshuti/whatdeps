import argparse
import asyncio
from pathlib import Path

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)

from . import parser, reporter
from .console import console
from .inspector import PackageInspector

REQUIREMENTS_FILES = {
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-test.txt",
    "dev-requirements.txt",
    "prod-requirements.txt",
    "requirements.txt-prod",
    "test-requirements.txt",
}


def is_valid_dependency_file(path: Path) -> bool:
    if path.name == "pyproject.toml":
        return True

    return path.name in REQUIREMENTS_FILES


def parse_dependency_files(args: argparse.Namespace) -> tuple[set[str], set[str]]:
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exists")

        if not is_valid_dependency_file(file_path):
            raise ValueError(
                "Invalid python dependency specification file, search PEP(735) to learn more!"
            )
        if file_path.name == "pyproject.toml":
            prod_deps, other_deps = parser.parse_pyproject(file_path)
        else:
            prod_deps = parser.parse_requirements(file_path)
            other_deps = {}
    else:
        prod_deps, other_deps = parser.find_and_parse()
    return prod_deps, other_deps


def _scan_dependencies(args: argparse.Namespace) -> tuple[set[str], set[str], int]:
    """Parse dependency files under status spinner"""
    with console.status("[bold green]Scanning dependency files..."):
        prod_deps, other_deps = parse_dependency_files(args)

        return prod_deps, other_deps, len(prod_deps) + len(other_deps)


def _print_summary(prod_deps: set, other_deps: set, total: int) -> None:
    """
    Print human readable summary line
    """
    console.print(
        f"\n[bold cyan] Inspecting {total} packages[/bold cyan] "
        f"([green]{len(prod_deps)}[/green] production dependencies, [blue]{len(other_deps)}[/blue] other dependencies)",
    )


async def _inspect_packages(prod_deps: set, other_deps: set, total: int) -> list:
    """
    Fetch GitHub/PyPi metadata under a progress bar.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        auto_refresh=True,
        transient=True,
        expand=True,
    ) as progress:
        task = progress.add_task(
            "[cyan]Fetching metadata from PyPI and GitHub...", total=total
        )
        inspector = PackageInspector()
        all_packages = [(pkg, False) for pkg in prod_deps] + [
            (pkg, True) for pkg in other_deps
        ]
        return await inspector.inspect_all(all_packages, progress, task)


def run(args: argparse.Namespace) -> None:
    prod_deps, other_deps, total = _scan_dependencies(args)
    if total == 0:
        console.print("[yellow]Couldn't find dependencies[/yellow]")
        return
    _print_summary(prod_deps, other_deps, total)
    results = asyncio.run(_inspect_packages(prod_deps, other_deps, total))
    results.sort(key=lambda x: (x.is_dev_dependency, x.name.lower()))
    reporter.display_results(results, console)
