# zoomus

[![Build Status](https://img.shields.io/travis/prschmid/zoomus)](https://travis-ci.org/prschmid/zoomus)
[![PyPI Downloads](https://img.shields.io/pypi/dm/zoomus)](https://pypi.org/project/zoomus/)
[![Python Versions](https://img.shields.io/pypi/pyversions/zoomus)](https://pypi.org/project/zoomus/)
[![PyPI Version](https://img.shields.io/pypi/v/zoomus)](https://pypi.org/project/zoomus/)
[![PyPI License](https://img.shields.io/pypi/l/zoomus)](https://pypi.org/project/zoomus/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)

[https://github.com/prschmid/zoomus](https://github.com/prschmid/zoomus)

Python wrapper around the [Zoom.us](http://zoom.us) REST API v1 and v2.

This work is heavily inspired by the Ruby GEM of the same name, [Zoomus](https://github.com/mllocs/zoomus)

## Installation

### The easy way

```sh
pip install zoomus
```

## Compatibility

`zoomus` has been tested for Python 3.6, 3.7, and 3.8 using [Travis CI](https://travis-ci.org/prschmid/zoomus)

Note, as this library heavily depends on the [requests](https://pypi.org/project/requests/) library, official compatibility is limited to the official compatibility of `requests`.

## Example Usage

### Create the client v2 (default)

As Zoom's default is now the V2 API, the client will default to the V2 version of the API.

```python
import json
from zoomus import ZoomClient

client = ZoomClient('API_KEY', 'API_SECRET')

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

for user in user_list['users']:
    user_id = user['id']
    print(json.loads(client.meeting.list(user_id=user_id).content))
```

What one will note is that the returned object from a call using the client is a [requests](https://pypi.org/project/requests/) `Response` object. This is done so that if there is any error working with the API that one has complete control of handling all errors. As such, to actually get the list of users in the example above, one will have to load the JSON from the content of the `Response` object that is returned.

### Create the client v1

Zoom has yet to officially remove support for the V1 API, and so to use the V1 API one can instantiate a client as follows.

```python
import json
from zoomus import ZoomClient

client = ZoomClient('API_KEY', 'API_SECRET', version=1)

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

for user in user_list['users']:
    user_id = user['id']
    print(json.loads(client.meeting.list(host_id=user_id).content))
```

### Using with a manage context

```python
with ZoomClient('API_KEY', 'API_SECRET') as client:
    user_list_response = client.users.list()
    ...
```

## Available methods

* client.user.create(...)
* client.user.cust_create(...)
* client.user.update(...)*
* client.user.list(...)
* client.user.pending(...)
* client.user.get(...)
* client.user.get_by_email(...)

* client.meeting.get(...)
* client.meeting.end(...)
* client.meeting.create(...)
* client.meeting.delete(...)
* client.meeting.list(...)
* client.meeting.update(...)

* client.report.get_account_report(...)
* client.report.get_user_report(...)

* client.webinar.create(...)
* client.webinar.update(...)
* client.webinar.delete(...)
* client.webinar.list(...)
* client.webinar.get(...)
* client.webinar.end(...)
* client.webinar.register(...)

* client.phone.call_logs(...)
* client.phone.calling_plans(...)
* client.phone.numbers_get(...)
* client.phone.numbers_list(...)
* client.phone.users(...)

## Running the Tests

### Simple

First, make sure to install the testing requirements

```sh
pip install -r requirements-tests.txt
```

Then run the tests via nose

```sh
nosetests
```

## Contributing

Please see the [CONTRIBUTING.md](./CONTRIBUTING.md) for the contribution guidelines for this project.
