import pytest

from scrapyd_client import ScrapydClient, exceptions


@pytest.mark.parametrize('input, formatted', [
    ('schedule', 'https://api.host.com:6800/schedule.json'),
    ('test/schedule', 'https://api.host.com:6800/test/schedule.json'),
    ('/schedule', 'https://api.host.com:6800/schedule.json'),
])
def test_format_url(input, formatted, client: ScrapydClient):
    assert client._format_url(input) == formatted


def test_get_ok(mocked_http_client: ScrapydClient):
    mocked_http_client.m.get('https://api.host.com:6800/schedule.json', json={'status': 'ok'})
    assert mocked_http_client.get('schedule') == {'status': 'ok'}


def test_http_auth(mocked_http_client: ScrapydClient):
    def check_auth(request, context):
        assert 'Authorization' in request.headers.keys()
        assert request.headers['Authorization'] == 'Basic cjAwdDpwYXNz'  # should be basic auth for r00t/pass
        return {
            'status': 'ok',
        }

    mocked_http_client.m.get('https://api.host.com:6800/schedule.json', json=check_auth)
    mocked_http_client.get('schedule')


def test_no_http_auth(mocked_http_client: ScrapydClient, monkeypatch):
    def check_no_auth(request, context):
        assert 'Authorization' not in request.headers.keys()
        return {
            'status': 'ok',
        }

    monkeypatch.setattr(mocked_http_client, 'auth', None)

    mocked_http_client.m.get('https://api.host.com:6800/schedule.json', json=check_no_auth)
    mocked_http_client.get('schedule')


def test_unauthorized(mocked_http_client: ScrapydClient):
    mocked_http_client.m.get('https://api.host.com:6800/schedule.json', status_code=401)
    with pytest.raises(exceptions.ScrapydUnAuthorizedException):
        mocked_http_client.get('schedule')


def test_bad_server_response(mocked_http_client: ScrapydClient):
    mocked_http_client.m.get('https://api.host.com:6800/schedule.json', status_code=502)
    with pytest.raises(exceptions.ScrapydClientHTTPException):
        mocked_http_client.get('schedule')
