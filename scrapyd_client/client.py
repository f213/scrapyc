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
        response = self.get('listprojects')
        self._assert_status_is_ok(response)
        for project in response.get('projects', []):
            yield project

    def _format_url(self, endpoint: str) -> str:
        """Append the API host"""
        return (self.host + '/%s.json' % endpoint).replace('//', '/').replace(':/', '://')

    def get(self, url: str) -> dict:
        """Do a GET request"""
        r = requests.get(self._format_url(url), auth=self.auth, timeout=TIMEOUT)
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
            raise exceptions.ScrapydUnAuthorizedException()

        if response.status_code != expected_status_code:
            raise exceptions.ScrapydClientHTTPException('Got response code %d, expected %d, error: %s' % (response.status_code, expected_status_code, response.text))

    def _assert_status_is_ok(self, response: dict):
        print(response)
        if 'status' not in response.keys() or response['status'] != 'ok':
            raise exceptions.ScrapydClientResponseNotOKException('Got bad server response: %s' % response)
