"""
Module to manage CANDY HOUSE API.
"""
import logging
import json
import requests

API_URL = 'https://api.candyhouse.co/v1'
API_LOGIN_ENDPOINT = '/accounts/login'
API_SESAME_ENDPOINT = '/sesames'
API_AUTH_HEADER = 'X-Authorization'

logger = logging.getLogger(__name__)

class CandyHouseAccount(object):
    """Representation of a CANDY HOUSE account."""
    api_url = API_URL
    auth_token = None
    email = None
    password = None

    def __init__(self, email, password, api_url=None, timeout=5):
        """Initialise the account object."""
        if api_url != None:
            self.api_url = api_url
        self.login(email, password, timeout=timeout)

    def login(self, email=None, password=None, session=None, timeout=5):
        """Log in to CANDY HOUSE account. Return True on success."""
        if email != None:
            self.email = email
        if password != None:
            self.password = password
        if session == None:
            session = requests.Session()

        url = self.api_url + API_LOGIN_ENDPOINT
        data = json.dumps({'email': self.email, 'password': self.password})
        headers = {'Content-Type': 'application/json'}
        response = None

        try:
            response = session.post(url, data=data, headers=headers,
                                    timeout=timeout)
        except requests.exceptions.ConnectionError:
            logger.warning("Unable to connect to %s", url)
        except requests.exceptions.Timeout:
            logger.warning("No response from %s", url)

        if response != None:
            if response.status_code == 200:
                self.auth_token = json.loads(response.text)['authorization']
                return True
            else:
                logger.warning("Login failed for %s: %s", self.email,
                               response.text)
        else:
            logger.warning("Login failed for %s", self.email)

        return False

    def request(self, method, endpoint, data=None, payload=None, timeout=5):
        """Send request to API."""
        session = requests.Session()
        url = self.api_url + endpoint
        headers = {}

        if payload != None:
            data = json.dumps(payload)
            headers['Content-Type'] = 'application/json'

        try:
            if self.auth_token != None:
                headers[API_AUTH_HEADER] = self.auth_token
                response = session.request(method, url, data=data,
                                           headers=headers, timeout=timeout)
                if response.status_code != 401:
                    return response

            logger.debug("Renewing auth token")
            if not self.login(session=session, timeout=timeout):
                return None

            # Retry  request
            headers[API_AUTH_HEADER] = self.auth_token
            return session.request(method, url, data=data, headers=headers,
                                   timeout=timeout)
        except requests.exceptions.ConnectionError:
            logger.warning("Unable to connect to %s", url)
        except requests.exceptions.Timeout:
            logger.warning("No response from %s", url)

        return None

    @property
    def sesames(self):
        """Return list of Sesames."""
        response = self.request('GET', API_SESAME_ENDPOINT)
        if response != None and response.status_code == 200:
            return json.loads(response.text)['sesames']

        logger.warning("Unable to list Sesames")
        return []
