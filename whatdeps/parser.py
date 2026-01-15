from pathlib import Path

import tomllib


def get_package_name(dep_spec: str) -> str:
    """Extract clean package name from dependency specification

    Examples:
        >>> get_package_name("requests>=2.28.0")
        'requests'
        >>> get_package_name("click[shell]")
        'click'
    """
    name = dep_spec.split(";")[0]
    name = name.split("[")[0]
    for op in ["==", ">=", "<=", ">", "<", "~=", "!="]:
        name = name.split(op)[0]
    return name.strip()


def parse_pyproject(path: Path) -> tuple[list[str], list[str]]:
    """Extract production and dev dependencies from pyproject.toml

    Args:
        path: Path to pyproject.toml file

    Returns:
        Tuple of (production_packages, dev_packages)
    """
    with open(path, "rb") as f:
        data = tomllib.load(f)

    # Production dependencies
    prod_deps = data.get("project", {}).get("dependencies", [])
    prod_packages = [get_package_name(dep) for dep in prod_deps]

    #  dependency-groups (PEP 735)
    dev_packages = []
    dep_groups = data.get("dependency-groups", {})
    for group_name, deps in dep_groups.items():
        dev_packages.extend([get_package_name(dep) for dep in deps])

    # Also check tool.hatch.envs.*.dependencies
    hatch_envs = data.get("tool", {}).get("hatch", {}).get("envs", {})
    for env_name, env_config in hatch_envs.items():
        if env_name != "default":  # Skip default env
            env_deps = env_config.get("dependencies", [])
            dev_packages.extend([get_package_name(dep) for dep in env_deps])

    poetry_groups = data.get("tool", {}).get("poetry", {})
    main_deps = poetry_groups.get("dependencies", {})
    if "python" in main_deps:
        del main_deps["python"]
    prod_packages.extend(main_deps.keys())

    # dev-dependencies
    legacy_dev_deps = poetry_groups.get("dev-dependencies", {})
    dev_packages.extend(legacy_dev_deps.keys())

    # Poetry >=1.2
    groups = poetry_groups.get("group", {})
    for group_name, group_config in groups.items():
        group_deps = group_config.get("dependencies", {})
        if group_name == "dev":
            dev_packages.extend(group_deps.keys())
        else:
            dev_packages.extend(group_deps.keys())

    return prod_packages, dev_packages


def parse_requirements(path: Path) -> list[str]:
    """Extract dependencies from requirements.txt

    Args:
        path: Path to requirements.txt file

    Returns:
        List of package names
    """
    packages = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            # Skip comments, empty lines, and -e/--editable installs
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            pkg = get_package_name(line)
            if pkg:
                packages.append(pkg)
    return packages


def find_and_parse() -> tuple[list[str], list[str]]:
    """Auto-detect and parse dependency files in current directory

    Returns:
        Tuple of (production_packages, dev_packages)

    Raises:
        FileNotFoundError: If no dependency files found
    """
    pyproject = Path("pyproject.toml")
    requirements = Path("requirements.txt")
    requirements_dev = Path("requirements-dev.txt")

    prod_deps = []
    dev_deps = []

    if pyproject.exists():
        prod_deps, dev_deps = parse_pyproject(pyproject)
    elif requirements.exists():
        prod_deps = parse_requirements(requirements)

    # requirements-dev.txt
    if requirements_dev.exists():
        dev_deps.extend(parse_requirements(requirements_dev))

    # some other possible dev requirements
    for pattern in [
        "requirements-test.txt",
        "requirements_dev.txt",
        "dev-requirements.txt",
    ]:
        dev_file = Path(pattern)
        if dev_file.exists():
            dev_deps.extend(parse_requirements(dev_file))

    if not prod_deps and not dev_deps:
        raise FileNotFoundError("No dependency files found")

    return prod_deps, dev_deps
