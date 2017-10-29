import pytest

from scrapyd_client import ScrapydClient, exceptions


def test_list_projects(mocked_http_client: ScrapydClient, response):
    mocked_http_client.m.get('https://api.host.com:6800/listprojects.json', json=response('listprojects'))

    got = list(mocked_http_client.list_projects())
    assert len(got) == 11
    assert 'pik' in got


def test_list_projects_fail(mocked_http_client: ScrapydClient, response):
    json = response('listprojects')
    json['status'] = 'FAIL U R A L00ZER'
    mocked_http_client.m.get('https://api.host.com:6800/listprojects.json', json=json)

    with pytest.raises(exceptions.ScrapydClientResponseNotOKException):
        list(mocked_http_client.list_projects())
