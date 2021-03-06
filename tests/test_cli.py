# -*- coding: utf-8 -*-
import click
import pytest

from scrapyc import cli


def test_status_command(mocked_http_client, response, runner):
    result = runner.invoke(cli.status, obj=dict(client=mocked_http_client))
    assert 'OK' in result.output
    assert '8f3b385b77dc' in result.output  # node name


def test_schedule_command(mocked_http_client, response, runner):
    mocked_http_client.m.post('https://api.host.com:6800/schedule.json', json=response('schedule'))

    result = runner.invoke(cli.schedule, ['testprj'], obj=dict(client=mocked_http_client))

    assert 'OK' in result.output
    assert 'https://api.host.com:6800' in result.output  # log-link
    assert 'a4c75a26bd4411e795c70242ac120002' in result.output  # jobid is present in the log-link


def test_unknown_project_when_scheduling(mocked_http_client, response, runner):
    mocked_http_client.m.post('https://api.host.com:6800/schedule.json', json=response('project_does_not_exist'))
    result = runner.invoke(cli.schedule, ['testprj'], obj=dict(client=mocked_http_client))

    assert '"testprj" does not exist' in result.output


def test_unknown_spider_when_scheduling(mocked_http_client, response, runner):
    mocked_http_client.m.post('https://api.host.com:6800/schedule.json', json=response('spider_does_not_exist'))
    result = runner.invoke(cli.schedule, ['testprj'], obj=dict(client=mocked_http_client))

    assert '"spider" is not present in the project' in result.output


def test_url_validator_with_empty_url():
    with pytest.raises(click.UsageError):
        cli.validate_url(None, None, None)


def test_url_validator_with_malformed_url():
    with pytest.raises(click.BadParameter):
        cli.validate_url(None, None, 'ev1l')


def test_list_projects(mocked_http_client, response, runner):
    mocked_http_client.m.get('https://api.host.com:6800/listprojects.json', json=response('listprojects'))
    result = runner.invoke(cli.projects, obj=dict(client=mocked_http_client))

    assert 'etaloninvest' in result.output


def test_list_spiders_ok(mocked_http_client, response, runner):
    mocked_http_client.m.get('https://api.host.com:6800/listspiders.json', json=response('listspiders'))
    result = runner.invoke(cli.spiders, ['prj'], obj=dict(client=mocked_http_client))

    assert 'spider1' in result.output


def test_list_spiders_for_wrong_project(mocked_http_client, response, runner):
    mocked_http_client.m.get('https://api.host.com:6800/listspiders.json', json=response('project_does_not_exist'))
    result = runner.invoke(cli.spiders, ['prj'], obj=dict(client=mocked_http_client))

    assert '"prj" does not exist' in result.output
