from os import path
from typing import Callable

import pytest
import requests_mock
import simplejson as json
from click.testing import CliRunner

from scrapyc import cli as app
from scrapyc import ScrapydClient


@pytest.fixture
def client() -> ScrapydClient:
    """Configured instance of scrapyc"""
    return ScrapydClient(
        host='https://api.host.com:6800',
        username='r00t',
        password='pass',
    )


@pytest.fixture
def mocked_http_client(client) -> ScrapydClient:
    """Client with blocked requests and requests_mock injected to .m"""
    with requests_mock.Mocker() as m:
        client.m = m
        yield client


@pytest.fixture
def response() -> Callable[[str], dict]:
    """Fixture reader"""
    def read_file(f):
        with open(path.join('tests/fixtures/', f) + '.json') as fp:
            return json.load(fp)

    return read_file


@pytest.fixture
def runner() -> CliRunner:
    """Click test runner"""
    return CliRunner()


@pytest.fixture
def cli() -> app:
    """Instance of CLI for testing"""
    return app
