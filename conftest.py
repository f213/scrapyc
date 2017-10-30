from os import path
from typing import Callable

import pytest
import requests_mock
import simplejson as json

from scrapyc import ScrapydClient


@pytest.fixture
def client() -> ScrapydClient:
    return ScrapydClient(
        host='https://api.host.com:6800',
        username='r00t',
        password='pass',
    )


@pytest.fixture
def mocked_http_client(client) -> ScrapydClient:
    with requests_mock.Mocker() as m:
        client.m = m
        yield client


@pytest.fixture
def response() -> Callable[[str], dict]:
    def read_file(f):
        with open(path.join('tests/fixtures/', f) + '.json') as fp:
            return json.load(fp)

    return read_file
