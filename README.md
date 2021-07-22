# zoomus

[![Build Status](https://img.shields.io/travis/prschmid/zoomus)](https://travis-ci.com/prschmid/zoomus)
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

`zoomus` has been tested for Python 3.6, 3.7, and 3.8 using [Travis CI](https://travis-ci.com/github/prschmid/zoomus)

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

### Create the client for EU users needing GDPR compliance

Zoom has EU specific endpoints that can be used to meet GDPR compliance. In oder for youto make use of those, simply set the base_uri to the appropriate one when initializing the client. For more details on the Zoom API, please refer to the [Zoom API documentation](https://marketplace.zoom.us/docs/api-reference/introduction)

Caution, the EU endpoint will not function unless your account is an EU account and has been setup as such with Zoom.

```python
import json
from zoomus import ZoomClient

client = ZoomClient('API_KEY', 'API_SECRET', base_uri="https://eu01api-www4local.zoom.us/v2")
```

### Create the client v1

Zoom has yet to officially remove support for the V1 API, and so to use the V1 API one can instantiate a client as follows. Note, we have stopped support for the V1 API, so there is only limited functionality and no new V1 API functionality is likely to be added.

```python
import json
from zoomus import ZoomClient

client = ZoomClient('API_KEY', 'API_SECRET', version=1)
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
* client.user.check_email(...)
* client.user.update_email(...)
* client.user.list(...)
* client.user.pending(...)
* client.user.get(...)
* client.user.get_by_email(...)
* client.user.get_settings(...)
* client.user.update_settings(...)

* client.meeting.get(...)
* client.meeting.end(...)
* client.meeting.create(...)
* client.meeting.delete(...)
* client.meeting.list(...)
* client.meeting.update(...)
* client.meeting.add_registrant(...)
* client.meeting.list_registrants(...)
* client.meeting.update_registrant_status(...)
* client.meeting.update_status(...)

* client.report.get_account_report(...)
* client.report.get_user_report(...)

* client.webinar.create(...)
* client.webinar.update(...)
* client.webinar.delete(...)
* client.webinar.list(...)
* client.webinar.get(...)
* client.webinar.end(...)
* client.webinar.register(...)
* client.webinar.add_panelists(...)
* client.webinar.list_panelists(...)
* client.webinar.remove_panelists(...)

* client.phone.call_logs(...)
* client.phone.calling_plans(...)
* client.phone.numbers_get(...)
* client.phone.numbers_list(...)
* client.phone.users(...)

* client.group.list(...)
* client.group.create(...)
* client.group.get(...)
* client.group.delete(...)
* client.group.list_members(...)
* client.group.add_members(...)
* client.group.delete_member(...)

* client.room.list(...)
* client.room.create(...)
* client.room.get(...)
* client.room.get_settings(...)
* client.room.get_devices(...)
* client.room.delete(...)
* client.room.check_in_or_out(...)
* client.room.update(...)

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
