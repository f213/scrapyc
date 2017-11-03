# -*- coding: utf-8 -*-
from collections import OrderedDict

import requests
from requests.auth import HTTPBasicAuth

from . import exceptions

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


TIMEOUT = 3


class ScrapydClient:
    def __init__(self, host, username=None, password=None):
        self.host = host

        if username is not None and password is not None:
            self.auth = HTTPBasicAuth(username, password)
        else:
            self.auth = None

    def get_status(self):
        """Get scrapyd status"""
        response = self.get('daemonstatus')
        self._assert_status_is_ok(response)

        return OrderedDict(response.items())

    def list_projects(self):
        """List projects uploaded to scrapyd"""
        response = self.get('listprojects')
        self._assert_status_is_ok(response)
        for project in response.get('projects', []):
            yield project

    def list_spiders(self, project):
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

    def schedule(self, project, spider):
        """Schedule a job for given project and spider"""
        response = self.post('schedule', data=dict(
            project=project,
            spider=spider,
        ))
        try:
            self._assert_status_is_ok(response)
        except exceptions.ResponseNotOKException as e:
            if 'no active project' in str(e):
                raise exceptions.ProjectDoesNotExist('Project %s does not exist' % project)

            if ': spider' in str(e) and str(e).endswith('not found'):
                raise exceptions.SpiderDoesNotExist('Spider %s does not exist' % spider)

            raise

        return response

    def get_log_link(self, project, spider, job):
        """Build a link to the log for a given project, spider and job"""
        return urljoin(self.host, '/'.join(['logs', project, spider, job]) + '.log')

    def _format_url(self, endpoint):
        """Append the API host"""
        return urljoin(self.host, '%s.json' % endpoint)

    def get(self, url, **kwargs):
        """Do a GET request"""
        r = requests.get(self._format_url(url), auth=self.auth, params=kwargs, timeout=TIMEOUT)
        self._assert_response_is_ok(r, 200)

        return r.json()

    def post(self, url, data, expected_status_code=200):
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

    def _assert_status_is_ok(self, response):
        if 'status' not in response.keys():
            raise exceptions.ResponseNotOKException('Got bad server response: %s' % response)

        if response['status'] != 'ok':
            raise exceptions.ResponseNotOKException('Got non-ok server response: %s' % response.get('message', '<empty>'))
