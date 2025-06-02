import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import click
try:
    from rich.console import Console
    from rich.table import Table
except Exception:  # pragma: no cover - fallback for environments without rich
    class Table:  # type: ignore
        def __init__(self, title: str | None = None) -> None:
            self.title = title
            self.columns: List[str] = []
            self.rows: List[tuple[str, ...]] = []

        def add_column(self, name: str) -> None:
            self.columns.append(name)

        def add_row(self, *args: str) -> None:
            self.rows.append(tuple(args))

    class Console:  # type: ignore
        def print(self, table: Table) -> None:
            header = " | ".join(table.columns)
            print(header)
            for row in table.rows:
                print(" | ".join(row))


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


def _parse_template_line(line: str) -> Optional[Tuple[str, str, Dict[str, str]]]:
    """Parse a line from a template extracting metadata."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("export "):
        line = line[len("export ") :]
    if "=" not in line:
        return None
    key, rest = line.split("=", 1)
    comment = ""
    if "#" in rest:
        value, comment = rest.split("#", 1)
        value = value.strip()
        comment = comment.strip()
    else:
        value = rest.strip()
    metadata: Dict[str, str] = {}
    if comment:
        for part in comment.split("|"):
            if ":" not in part:
                continue
            k, v = part.split(":", 1)
            metadata[k.strip()] = v.strip()
    return key.strip(), value, metadata


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


@main.command()
@click.option("--template", type=click.Path(), help="Template file to read")
def create(template: str | None) -> None:
    """Create an environment file from a template."""
    base_dir = Path(os.getcwd())
    template_path = _find_template(base_dir, template)

    env_name = click.prompt(
        "Enter environment name", default="", show_default=False
    ).strip()
    if env_name in {"dist", "template"}:
        raise click.ClickException("Invalid environment name")

    env_file = ".env" if not env_name else f".env.{env_name}"
    env_path = base_dir / env_file

    existing_data: Dict[str, str] = {}
    if env_path.exists():
        action = click.prompt(
            f"{env_file} exists. Choose action",
            type=click.Choice(["cancel", "overwrite", "merge"]),
            default="cancel",
        )
        if action == "cancel":
            click.echo("Cancelled")
            return
        if action == "merge":
            existing_data = _parse_env_file(env_path)

    data = existing_data.copy()
    for line in template_path.read_text().splitlines():
        parsed = _parse_template_line(line)
        if not parsed:
            continue
        key, value, meta = parsed
        default_val = data.get(key, value)

        question = meta.get("question", f"Set a value for {key}")
        enum = meta.get("enum")
        typ = meta.get("type")

        prompt_text = question
        default_for_prompt = default_val if default_val != "" else ""

        prompt_type: click.ParamType | click.Choice | None = None
        if enum:
            choices = [c.strip() for c in enum.split(",")]
            prompt_type = click.Choice(choices)
        elif typ == "number":
            prompt_type = int if (default_val and default_val.isdigit()) else float
        elif typ == "bool":
            prompt_type = click.Choice(["True", "False"])

        resp = click.prompt(
            prompt_text,
            default=default_for_prompt,
            show_default=default_for_prompt != "",
            type=prompt_type,
        )
        data[key] = str(resp)

    with env_path.open("w") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")

    click.echo(f"Environment written to {env_file}")


if __name__ == "__main__":
    main()
