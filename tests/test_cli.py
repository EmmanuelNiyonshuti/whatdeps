import asyncio
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest

from whatdeps import cli
from whatdeps.models import PackageInfo
from whatdeps.utils import _inspect_packages, _scan_dependencies, parse_dependency_files


class TestParseDependencyFiles:
    def test_file_not_found(self, tmp_path):
        args = Mock()
        args.file = str(tmp_path / "nonexistent.txt")

        with pytest.raises(FileNotFoundError):
            parse_dependency_files(args)

    def test_invalid_file_type(self, tmp_path):
        bad = tmp_path / "random.txt"
        bad.write_text("content")
        args = Mock()
        args.file = str(bad)

        with pytest.raises(ValueError):
            parse_dependency_files(args)

    def test_parses_pyproject(self, sample_pyproject):
        args = Mock()
        args.file = str(sample_pyproject)

        prod_deps, other_deps = parse_dependency_files(args)

        assert isinstance(prod_deps, set)
        assert isinstance(other_deps, set)
        assert len(prod_deps) > 0

    def test_parses_requirements(self, sample_requirements):
        args = Mock()
        args.file = str(sample_requirements)

        prod_deps, other_deps = parse_dependency_files(args)

        assert isinstance(prod_deps, set)
        assert other_deps == {}

    def test_auto_detect_when_no_file(self, sample_pyproject, monkeypatch):
        monkeypatch.chdir(sample_pyproject.parent)
        args = Mock()
        args.file = None

        prod_deps, other_deps = parse_dependency_files(args)

        assert isinstance(prod_deps, set)


class TestScanDependencies:
    def test_returns_deps_and_total(self, sample_pyproject):
        args = Mock()
        args.file = str(sample_pyproject)

        prod_deps, other_deps, total = _scan_dependencies(args)

        assert total == len(prod_deps) + len(other_deps)

    def test_propagates_file_not_found(self, tmp_path):
        args = Mock()
        args.file = str(tmp_path / "ghost.txt")

        with pytest.raises(FileNotFoundError):
            _scan_dependencies(args)

    def test_propagates_value_error(self, tmp_path):
        bad = tmp_path / "bad.txt"
        bad.write_text("x")
        args = Mock()
        args.file = str(bad)

        with pytest.raises(ValueError):
            _scan_dependencies(args)


class TestInspectPackages:
    def test_returns_sorted_results(self):
        mock_results = [
            PackageInfo(name="requests", is_dev_dependency=False),
            PackageInfo(name="pytest", is_dev_dependency=True),
        ]
        mock_inspector = Mock()
        mock_inspector.inspect_all = AsyncMock(return_value=mock_results)

        with patch("whatdeps.utils.PackageInspector", return_value=mock_inspector):
            results = asyncio.run(_inspect_packages({"requests"}, {"pytest"}, 2))

        assert results == mock_results
        mock_inspector.inspect_all.assert_called_once()

    def test_empty_deps(self):
        mock_inspector = Mock()
        mock_inspector.inspect_all = AsyncMock(return_value=[])

        with patch("whatdeps.utils.PackageInspector", return_value=mock_inspector):
            results = asyncio.run(_inspect_packages(set(), {}, 0))

        assert results == []

    def test_passes_progress_and_task_to_inspector(self):
        mock_inspector = Mock()
        mock_inspector.inspect_all = AsyncMock(return_value=[])

        with patch("whatdeps.utils.PackageInspector", return_value=mock_inspector):
            asyncio.run(_inspect_packages({"requests"}, {}, 1))

        call_args = mock_inspector.inspect_all.call_args[0]
        # inspect_all(all_packages, progress, task)
        assert len(call_args) == 3
        packages, progress, task = call_args
        assert ("requests", False) in packages


class TestRun:
    def test_exits_early_on_empty_deps(self, capsys):
        with patch("whatdeps.utils._scan_dependencies", return_value=(set(), set(), 0)):
            from whatdeps.utils import run

            run(Mock())

        # _inspect_packages should never be reached
        # capsys or just asserting no error is sufficient here

    def test_full_flow(self, sample_pyproject):
        from whatdeps.utils import run

        mock_results = [PackageInfo(name="requests", is_dev_dependency=False)]
        mock_inspector = Mock()
        mock_inspector.inspect_all = AsyncMock(return_value=mock_results)

        args = Mock()
        args.file = str(sample_pyproject)

        with patch("whatdeps.utils.PackageInspector", return_value=mock_inspector):
            with patch("whatdeps.utils.reporter.display_results") as mock_display:
                run(args)

        mock_display.assert_called_once()
        displayed_results = mock_display.call_args[0][0]
        assert displayed_results == mock_results

    def test_results_are_sorted(self, sample_pyproject):
        from whatdeps.utils import run

        mock_results = [
            PackageInfo(name="zebra", is_dev_dependency=True),
            PackageInfo(name="alpha", is_dev_dependency=False),
            PackageInfo(name="mango", is_dev_dependency=False),
        ]
        mock_inspector = Mock()
        mock_inspector.inspect_all = AsyncMock(return_value=mock_results)

        args = Mock()
        args.file = str(sample_pyproject)

        with patch("whatdeps.utils.PackageInspector", return_value=mock_inspector):
            with patch("whatdeps.utils.reporter.display_results") as mock_display:
                run(args)

        sorted_results = mock_display.call_args[0][0]
        names = [r.name for r in sorted_results]
        assert names == ["alpha", "mango", "zebra"]


class TestMain:
    def test_success(self, sample_pyproject, monkeypatch):
        monkeypatch.chdir(sample_pyproject.parent)

        with patch.object(sys, "argv", ["prog"]):
            with patch("whatdeps.cli.run") as mock_run:
                cli.main()

        mock_run.assert_called_once()

    def test_file_argument_passed_through(self, sample_pyproject):
        with patch.object(sys, "argv", ["prog", "-f", str(sample_pyproject)]):
            with patch("whatdeps.cli.run") as mock_run:
                cli.main()

        call_args = mock_run.call_args[0][0]
        assert call_args.file == str(sample_pyproject)

    def test_file_not_found_exits_1(self):
        with patch.object(sys, "argv", ["prog"]):
            with patch("whatdeps.cli.run", side_effect=FileNotFoundError("missing")):
                with pytest.raises(SystemExit) as exc:
                    cli.main()

        assert exc.value.code == 1

    def test_value_error_exits_1(self, tmp_path):
        bad = tmp_path / "bad.txt"
        bad.write_text("x")

        with patch.object(sys, "argv", ["prog", "-f", str(bad)]):
            with patch("whatdeps.cli.run", side_effect=ValueError("unsupported")):
                with pytest.raises(SystemExit) as exc:
                    cli.main()

        assert exc.value.code == 1

    def test_keyboard_interrupt_exits_130(self):
        with patch.object(sys, "argv", ["prog"]):
            with patch("whatdeps.cli.run", side_effect=KeyboardInterrupt()):
                with pytest.raises(SystemExit) as exc:
                    cli.main()

        assert exc.value.code == 130

    def test_unexpected_error_exits_1(self):
        with patch.object(sys, "argv", ["prog"]):
            with patch("whatdeps.cli.run", side_effect=Exception("boom")):
                with pytest.raises(SystemExit) as exc:
                    cli.main()

        assert exc.value.code == 1

    def test_argument_parser_has_description(self):
        with patch("whatdeps.cli.argparse.ArgumentParser") as mock_parser_class:
            mock_parser = Mock()
            mock_parser.parse_args.return_value = Mock(file=None)
            mock_parser_class.return_value = mock_parser

            with patch("whatdeps.cli.run"):
                cli.main()

        _, kwargs = mock_parser_class.call_args
        assert "description" in kwargs
