from scrapyc import cli


def test_status_command(mocked_http_client, response, runner):
    mocked_http_client.m.get('https://api.host.com:6800/daemonstatus.json', json=response('daemonstatus'))
    result = runner.invoke(cli.status, obj=dict(client=mocked_http_client))
    assert 'OK' in result.output
    assert '8f3b385b77dc' in result.output  # node name
