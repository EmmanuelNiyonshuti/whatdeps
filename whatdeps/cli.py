import argparse
import asyncio
import sys
from pathlib import Path

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)

from . import parser, reporter
from .inspector import PackageInspector


async def async_main(args):
    """Async main entry point"""
    console = Console()

    try:
        # Parse dependencies
        with console.status("[bold green]Scanning dependency files...", spinner="dots"):
            if args.file:
                path = Path(args.file)
                if path.name == "pyproject.toml":
                    prod_packages, dev_packages = parser.parse_pyproject(path)
                else:
                    prod_packages = parser.parse_requirements(path)
                    dev_packages = []
            else:
                prod_packages, dev_packages = parser.find_and_parse()

        total = len(prod_packages) + len(dev_packages)
        if total == 0:
            console.print("[yellow]No dependencies found[/yellow]")
            return

        # Prepare package list
        all_packages = [(pkg, False) for pkg in prod_packages] + [
            (pkg, True) for pkg in dev_packages
        ]

        # Scan site-packages
        inspector = PackageInspector()

        # Inspect packages with progress bar
        console.print(
            f"\n[bold cyan] Inspecting {total} packages[/bold cyan] "
            f"([green]{len(prod_packages)}[/green] prod, [blue]{len(dev_packages)}[/blue] dev)"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(
                "[cyan]Fetching metadata from PyPI and GitHub...", total=total
            )
            results = await inspector.inspect_all(all_packages, progress, task)

        # Sort and display results
        results.sort(key=lambda x: (x.is_dev_dependency, x.name.lower()))
        reporter.display_results(results, console)

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}", style="bold")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point"""
    parser_obj = argparse.ArgumentParser(
        description="Inspect Python package metadata and health",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_obj.add_argument(
        "-f",
        "--file",
        help="Path to pyproject.toml or requirements.txt (auto-detect if not specified)",
    )

    args = parser_obj.parse_args()

    # Run async main
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
