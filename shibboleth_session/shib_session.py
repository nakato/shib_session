from html.parser import HTMLParser
import re

import requests

class ShibSession(requests.Session):

    def __init__(self, username: str, password: str,
                 login_url: str,
                 idp_url: str = None) -> None:
        super(ShibSession, self).__init__()
        self.username = username
        self.password = password
        self.login_url = login_url
        self.idp_url = idp_url
        self._authenticate()

    def _authenticate(self):
        login_req = self.get(self.login_url, allow_redirects=False)
        login_req_forward = login_req.headers['Location']  # Can fail
        if not (self.idp_url and login_req_forward.startswith(self.idp_url)):
            raise Exception()  # SAMLAuthError.InsecureRedirect
        login_assert = requests.get(login_req_forward, allow_redirects=False)
        saml_cookies = login_assert.cookies
        login_page = login_assert.headers['Location']  # Can fail
        # Yes, this get is required.  Shib does not like POST without first
        # performing a get.
        requests.get(login_page, cookies=saml_cookies, allow_redirects=False)
        login_data = {
            'j_username': self.username,
            'j_password': self.password,
            'donotcache': 1,
            '_eventId_proceed': 'submit',
            }
        login_post = requests.post(login_page, data=login_data,
                                   allow_redirects=False,
                                   cookies=saml_cookies)
        if login_post.status_code != 200:
            raise Exception()  # SAMLAuthError.LoginFailed
        login_post_contnet = login_post.content.decode('UTF-8')
        assert_url_rm = re.search(
            '<form action="(.*?)" method="post">', login_post_contnet)
        relay_state_rm = re.search(
            '<input type="hidden" name="RelayState" value="(.*?)"/>',
            login_post_contnet)
        saml_response_rm = re.search(
            '<input type="hidden" name="SAMLResponse" value="(.*?)"/>',
            login_post_contnet)
        if not (assert_url_rm and relay_state_rm and saml_response_rm):
            # SAMLAuthError.LoginFailed (Forward SAML assertion missing)
            raise Exception() 
        hp = HTMLParser()
        assert_url = hp.unescape(assert_url_rm[1])
        relay_state = hp.unescape(relay_state_rm[1])
        # Base64 data, don't need to unescape
        saml_response = saml_response_rm[1]
        assert_data = {
            'RelayState': relay_state,
            'SAMLResponse': saml_response,
        }
        assert_post = self.post(assert_url, data=assert_data,
                                allow_redirects=False)
        if not assert_post.ok:
            raise Exception()  # SP failed to accept assert
