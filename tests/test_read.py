import pytest

from scrapyc import ScrapydClient, exceptions


def test_list_projects(mocked_http_client: ScrapydClient, response):
    mocked_http_client.m.get('https://api.host.com:6800/listprojects.json', json=response('listprojects'))

    got = list(mocked_http_client.list_projects())
    assert len(got) == 11
    assert 'pik' in got


def test_list_projects_fail(mocked_http_client: ScrapydClient, response):
    json = response('listprojects')
    json['status'] = 'FAIL U R A L00ZER'
    mocked_http_client.m.get('https://api.host.com:6800/listprojects.json', json=json)

    with pytest.raises(exceptions.ResponseNotOKException):
        list(mocked_http_client.list_projects())


def test_list_spiders(mocked_http_client: ScrapydClient, response):
    mocked_http_client.m.get('https://api.host.com:6800/listspiders.json', json=response('listspiders'))

    got = list(mocked_http_client.list_spiders('pik'))
    assert got == ['spider1', 'spider2']


def test_bad_project_name(mocked_http_client: ScrapydClient, response):
    mocked_http_client.m.get('https://api.host.com:6800/listspiders.json', json=response('project_does_not_exist'))

    with pytest.raises(exceptions.ProjectDoesNotExist):
        list(mocked_http_client.list_spiders('nonexistant'))


def test_list_spiders_bad_response(mocked_http_client: ScrapydClient):
    """
    Check if non bad-project-name errors raise more common exception
    """
    mocked_http_client.m.get('https://api.host.com:6800/listspiders.json', json={'status': 'Я вас не знаю, идите нахер'})

    with pytest.raises(exceptions.ResponseNotOKException):
        list(mocked_http_client.list_spiders('stuff'))
