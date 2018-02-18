# Shibboleth Session

Intended as a wrapper to make Shibboleth easy when you really need to log in
like a user with an application.


## Installation

`pip install git+https://.../shibboleth_session.git`


## Usage:

```
from shibboleth_session import ShibSession
import shibboleth_session

with ShibSession('username', 'password', 'https://that.site/login',
                 idp_url='https://login.shibboleth') as sess:
    r = sess.get('http://that.site/protected/page')
```

See http://docs.python-requests.org/en/master/user/advanced/#session-objects


## Notes:

1. There are no tests
   * Feel free to propose tests
2. It probably only works for new Shibs that haven't been modified too much
   * SAML login flows can be a bit custom.
   * Doesn't support consent flows.
