from pathlib import Path

from click.testing import CliRunner

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
        assert cli.EMOJI_EMPTY in result.output
        assert cli.EMOJI_CHECK in result.output
