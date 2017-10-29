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

    def _format_url(self, endpoint):
        """Append the API host"""
        return (self.host + '/%s.json' % endpoint).replace('//', '/').replace(':/', '://')

    def get(self, url):
        """Do a GET request"""
        r = requests.get(self._format_url(url), auth=self.auth, timeout=TIMEOUT)
        self._check_response(r, 200)

        return r.json()

    def _check_response(self, response, expected_status_code):
        """Check sever response and raise exception if it is bad"""
        if response.status_code == 401:
            raise exceptions.ScrapydUnAuthorizedException()

        if response.status_code != expected_status_code:
            raise exceptions.ScrapydClientHTTPException('Got response code %d, expected %d, error: %s' % (response.status_code, expected_status_code, response.text))
