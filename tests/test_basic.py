from pathlib import Path
import os
import sys

from click.testing import CliRunner

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from envzilla import cli


def test_main_runs():
    runner = CliRunner()
    result = runner.invoke(cli.main, ["--help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output


def test_list_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path(".env.dist").write_text("VAR1=\nVAR2=1\n")
        Path(".env").write_text("VAR2=foo\n")
        result = runner.invoke(cli.main, ["list"])
        assert result.exit_code == 0
        assert "VAR1" in result.output
        assert "VAR2" in result.output
        assert cli.EMOJI_MISSING in result.output
        assert cli.EMOJI_CHECK in result.output
