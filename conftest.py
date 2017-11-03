from os import path

import pytest
import requests_mock
import simplejson as json
from click.testing import CliRunner

from scrapyc import ScrapydClient


@pytest.fixture
def client():
    """Configured instance of scrapyc"""
    return ScrapydClient(
        host='https://api.host.com:6800',
        username='r00t',
        password='pass',
    )


@pytest.fixture
def mocked_http_client(client, response):
    """Client with blocked requests and requests_mock injected to .m"""
    with requests_mock.Mocker() as m:
        client.m = m
        client.m.get('https://api.host.com:6800/daemonstatus.json', json=response('daemonstatus'))
        yield client


@pytest.fixture
def response():
    """Fixture reader"""
    def read_file(f):
        with open(path.join('tests/fixtures/', f) + '.json') as fp:
            return json.load(fp)

    return read_file


@pytest.fixture
def runner():
    """Click test runner"""
    return CliRunner(env=dict(
        SCRAPYC_URL='https://api.host.com:6800',
        SCRAPYC_USERNAME='r00t',
        SCRAPYC_PASSWORD='pass',
    ))
