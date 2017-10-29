import pytest
import requests_mock

from scrapyd_client import ScrapydClient


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
