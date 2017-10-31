def test_cli_runs(cli, runner):
    result = runner.invoke(cli.cli, '--help')
    assert len(result.output) > 100
