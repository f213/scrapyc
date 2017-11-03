# -*- coding: utf-8 -*-
import pytest

from scrapyc import exceptions


def test_bad_project_name(mocked_http_client, response):
    mocked_http_client.m.post('https://api.host.com:6800/schedule.json', json=response('project_does_not_exist'))

    with pytest.raises(exceptions.ProjectDoesNotExist):
        mocked_http_client.schedule(project='nonexistant', spider='spider')


def test_bad_spider_name(mocked_http_client, response):
    mocked_http_client.m.post('https://api.host.com:6800/schedule.json', json=response('spider_does_not_exist'))

    with pytest.raises(exceptions.SpiderDoesNotExist):
        mocked_http_client.schedule(project='existant', spider='nonexistant')


def test_schedule_ok(mocked_http_client, response):
    mocked_http_client.m.post('https://api.host.com:6800/schedule.json', json=response('schedule'))

    got = mocked_http_client.schedule(project='stuff', spider='stuff')
    assert got['jobid'] == 'a4c75a26bd4411e795c70242ac120002'
