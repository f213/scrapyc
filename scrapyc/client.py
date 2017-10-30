from typing import Generator

import requests
from requests.auth import HTTPBasicAuth

from . import exceptions

TIMEOUT = 3


class ScrapydClient:
    def __init__(self, host: str, username: str=None, password: str=None):
        self.host = host

        if username is not None and password is not None:
            self.auth = HTTPBasicAuth(username, password)
        else:
            self.auth = None

    def list_projects(self) -> Generator[str, None, None]:
        """List projects uploaded to scrapyd"""
        response = self.get('listprojects')
        self._assert_status_is_ok(response)
        for project in response.get('projects', []):
            yield project

    def list_spiders(self, project: str) -> Generator[str, None, None]:
        """List spiders for a project"""
        response = self.get('listspiders', project=project)

        try:
            self._assert_status_is_ok(response)
        except exceptions.ResponseNotOKException as e:
            if 'no active project' in str(e):
                raise exceptions.ProjectDoesNotExist('Project %s does not exist' % project)
            raise

        for spider in response.get('spiders', []):
            yield spider

    def _format_url(self, endpoint: str) -> str:
        """Append the API host"""
        return (self.host + '/%s.json' % endpoint).replace('//', '/').replace(':/', '://')

    def get(self, url: str, **kwargs) -> dict:
        """Do a GET request"""
        r = requests.get(self._format_url(url), auth=self.auth, params=kwargs, timeout=TIMEOUT)
        self._assert_response_is_ok(r, 200)

        return r.json()

    def post(self, url: str, data: dict, expected_status_code=200) -> dict:
        """Do a POST request"""
        r = requests.post(self._format_url(url), data=data, auth=self.auth, timeout=TIMEOUT)
        self._assert_response_is_ok(r, expected_status_code)

        return r.json()

    def _assert_response_is_ok(self, response, expected_status_code):
        """Check sever response and raise exception if it is bad"""
        if response.status_code == 401:
            raise exceptions.UnAuthorizedException()

        if response.status_code != expected_status_code:
            raise exceptions.HTTPException('Got response code %d, expected %d, error: %s' % (response.status_code, expected_status_code, response.text))

    def _assert_status_is_ok(self, response: dict):
        if 'status' not in response.keys():
            raise exceptions.ResponseNotOKException('Got bad server response: %s' % response)

        if response['status'] != 'ok':
            raise exceptions.ResponseNotOKException('Got non-ok server response: %s' % response.get('message', '<empty>'))