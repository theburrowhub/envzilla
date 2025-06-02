import os
from pathlib import Path
from typing import Dict, List

import click
from rich.console import Console
from rich.table import Table


EMOJI_CHECK = "✅"
EMOJI_MISSING = "❌"
EMOJI_EMPTY = "⚠️"

console = Console()


def _parse_env_file(path: Path) -> Dict[str, str]:
    """Parse a .env style file into a dictionary."""
    data: Dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def _find_template(base_dir: Path, template: str | None) -> Path:
    if template:
        path = base_dir / template
        if not path.exists():
            raise click.ClickException(f"Template file {template} not found")
        return path
    for name in (".env.dist", ".env.template"):
        path = base_dir / name
        if path.exists():
            return path
    raise click.ClickException("Template file not found (.env.dist or .env.template)")


def _find_env_files(base_dir: Path, template_path: Path) -> List[Path]:
    files: List[Path] = []
    for path in base_dir.glob(".env*"):
        if path == template_path:
            continue
        if path.suffix in {".dist", ".template"}:
            continue
        files.append(path)
    files.sort()
    return files


@click.group()
def main() -> None:
    """envzilla CLI."""
    pass


@main.command()
@click.option("--template", type=click.Path(), help="Template file to read")
@click.option("--only-missing", is_flag=True, help="Show only missing or empty variables")
def list(template: str | None, only_missing: bool) -> None:  # noqa: D401
    """List environment variables across files."""
    base_dir = Path(os.getcwd())
    template_path = _find_template(base_dir, template)
    env_files = _find_env_files(base_dir, template_path)

    template_vars = _parse_env_file(template_path)
    env_data = {f.name: _parse_env_file(f) for f in env_files}

    table = Table(title="Environment variables")
    table.add_column("Variable")
    for f in env_files:
        table.add_column(f.name)

    for var in sorted(template_vars):
        statuses = []
        for f in env_files:
            values = env_data[f.name]
            if var not in values:
                statuses.append(EMOJI_MISSING)
            else:
                statuses.append(EMOJI_CHECK if values[var] else EMOJI_EMPTY)
        if only_missing and all(s == EMOJI_CHECK for s in statuses):
            continue
        table.add_row(var, *statuses)

    console.print(table)


if __name__ == "__main__":
    main()
