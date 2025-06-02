from pathlib import Path
import os
import sys
from click.testing import CliRunner

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from envzilla import cli


def test_create_basic():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path(".env.dist").write_text("VAR1=foo\nVAR2=2 #question:Value two|type:number\n")
        inputs = "\n\n3\n"  # env name empty, VAR1 default, VAR2=3
        result = runner.invoke(cli.main, ["create"], input=inputs)
        assert result.exit_code == 0
        assert Path(".env").read_text() == "VAR1=foo\nVAR2=3\n"


def test_create_merge_existing():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path(".env.dist").write_text("VAR1=a\nVAR2=b\n")
        Path(".env").write_text("VAR1=x\n")
        inputs = "\nmerge\n\n\n"  # env name empty, merge, keep VAR1, default for VAR2
        result = runner.invoke(cli.main, ["create"], input=inputs)
        assert result.exit_code == 0
        assert Path(".env").read_text() == "VAR1=x\nVAR2=b\n"


def test_create_custom_name():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path(".env.dist").write_text("VAR1=\n")
        inputs = "test\n\n"  # env name 'test', VAR1 blank
        result = runner.invoke(cli.main, ["create"], input=inputs)
        assert result.exit_code == 0
        assert Path(".env.test").exists()
