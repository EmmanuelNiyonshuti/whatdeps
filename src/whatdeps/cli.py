import argparse
import sys

from . import __version__
from .console import console
from .utils import run


def main() -> None:
    parser_obj = argparse.ArgumentParser(
        description="Get to know about your Python project dependency informations from PyPi and GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_obj.add_argument(
        "-f",
        "--file",
        help="Path to pyproject.toml or requirements.txt (will auto-detect if not specified)",
    )
    parser_obj.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser_obj.parse_args()
    try:
        run(args)
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]", style="bold")
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red] {e}[/red]", style="bold")
        sys.exit(1)
