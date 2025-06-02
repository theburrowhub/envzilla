from envzilla import cli

def test_main_runs(capsys):
    cli.main([])
    captured = capsys.readouterr()
    assert 'envzilla is ready!' in captured.out
