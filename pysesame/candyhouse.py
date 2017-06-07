"""
Module to manage CANDY HOUSE API.
"""
import logging
import json
import requests

API_URL = 'https://api.candyhouse.co/v1'
API_LOGIN_ENDPOINT = '/accounts/login'
API_SESAME_LIST_ENDPOINT = '/sesames'
API_AUTH_HEADER = 'X-Authorization'

_LOGGER = logging.getLogger(__name__)


class CandyHouseAccount(object):
    """Representation of a CANDY HOUSE account."""

    api_url = API_URL
    auth_token = None
    email = None
    password = None
    session = None

    def __init__(self, email, password, api_url=None, timeout=5):
        """Initialise the account object."""
        self.session = requests.Session()
        if api_url is not None:
            self.api_url = api_url
        self.login(email, password, timeout=timeout)

    def login(self, email=None, password=None, timeout=5):
        """Log in to CANDY HOUSE account. Return True on success."""
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password

        url = self.api_url + API_LOGIN_ENDPOINT
        data = json.dumps({'email': self.email, 'password': self.password})
        headers = {'Content-Type': 'application/json'}
        response = None

        try:
            response = self.session.post(url, data=data, headers=headers,
                                         timeout=timeout)
        except requests.exceptions.ConnectionError:
            _LOGGER.warning("Unable to connect to %s", url)
        except requests.exceptions.Timeout:
            _LOGGER.warning("No response from %s", url)

        if response is not None:
            if response.status_code == 200:
                self.auth_token = json.loads(response.text)['authorization']
                return True
            else:
                _LOGGER.warning("Login failed for %s: %s", self.email,
                                response.text)
        else:
            _LOGGER.warning("Login failed for %s", self.email)

        return False

    def request(self, method, endpoint, payload=None, timeout=5):
        """Send request to API."""
        url = self.api_url + endpoint
        data = None
        headers = {}

        if payload is not None:
            data = json.dumps(payload)
            headers['Content-Type'] = 'application/json'

        try:
            if self.auth_token is not None:
                headers[API_AUTH_HEADER] = self.auth_token
                response = self.session.request(method, url, data=data,
                                                headers=headers,
                                                timeout=timeout)
                if response.status_code != 401:
                    return response

            _LOGGER.debug("Renewing auth token")
            if not self.login(timeout=timeout):
                return None

            # Retry  request
            headers[API_AUTH_HEADER] = self.auth_token
            return self.session.request(method, url, data=data,
                                        headers=headers,
                                        timeout=timeout)
        except requests.exceptions.ConnectionError:
            _LOGGER.warning("Unable to connect to %s", url)
        except requests.exceptions.Timeout:
            _LOGGER.warning("No response from %s", url)

        return None

    @property
    def sesames(self):
        """Return list of Sesames."""
        response = self.request('GET', API_SESAME_LIST_ENDPOINT)
        if response is not None and response.status_code == 200:
            return json.loads(response.text)['sesames']

        _LOGGER.warning("Unable to list Sesames")
        return []
