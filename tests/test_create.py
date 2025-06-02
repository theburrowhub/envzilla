"""Tests for the ``create`` command."""

from pathlib import Path

from click.testing import CliRunner
from envzilla import cli


def test_create_basic() -> None:
    """Creating a file from a template works with defaults."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path(".env.dist").write_text(
            "VAR1=foo\nVAR2=2 #question:Value two|type:number\n",
            encoding="utf-8",
        )
        inputs = "\n\n3\n"  # env name empty, VAR1 default, VAR2=3
        result = runner.invoke(cli.main, ["create"], input=inputs)
        assert result.exit_code == 0
        assert Path(".env").read_text(encoding="utf-8") == "VAR1=foo\nVAR2=3\n"


def test_create_merge_existing() -> None:
    """Merging with an existing file preserves previous values."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path(".env.dist").write_text("VAR1=a\nVAR2=b\n", encoding="utf-8")
        Path(".env").write_text("VAR1=x\n", encoding="utf-8")
        inputs = "\nmerge\n\n\n"  # env name empty, merge, keep VAR1, default for VAR2
        result = runner.invoke(cli.main, ["create"], input=inputs)
        assert result.exit_code == 0
        assert Path(".env").read_text(encoding="utf-8") == "VAR1=x\nVAR2=b\n"


def test_create_custom_name() -> None:
    """Custom environment file names are respected."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path(".env.dist").write_text("VAR1=\n", encoding="utf-8")
        inputs = "test\n\n"  # env name 'test', VAR1 blank
        result = runner.invoke(cli.main, ["create"], input=inputs)
        assert result.exit_code == 0
        assert Path(".env.test").exists()
