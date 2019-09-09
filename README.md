# zoomus

[![Build Status](https://travis-ci.org/actmd/zoomus.svg?branch=master)](https://travis-ci.org/actmd/zoomus)

[https://github.com/actmd/zoomus](https://github.com/actmd/zoomus)

Python wrapper around the [Zoom.us](http://zoom.us) REST API v1 and v2.

This work is heavily inspired by the Ruby GEM of the same name, [Zoomus](https://github.com/mllocs/zoomus)

## Installation

### The easy way

```sh
pip install zoomus
```

## Compatibility

`zoomus` has been tested for Python 2.7, 3.4, 3.5, 3.6, 3.7, and pypy using [Travis CI](https://travis-ci.org/actmd/zoomus)

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

### Running the tests across multiple python versions in parallel

If you don't trust our [Travis CI](https://travis-ci.org/actmd/zoomus) badge above, you can run all of the tests across multiple python versions by using [pyenv](https://github.com/yyuu/pyenv), and [tox](https://pypi.python.org/pypi/tox).

Note: If you are using OS X and installed `pyenv` with brew, make sure to follow [these instructions](https://github.com/pyenv/pyenv#homebrew-on-macos) as well.

You'll want to make sure that you have all of the different python versions are installed so that they can be tested:

```sh
# Install the versions
pyenv install 2.7.10
pyenv install 3.4.3
pyenv install 3.5.0
pyenv install 3.6.0
pyenv install 3.7.0

# Set all these to be global versions
pyenv global system 2.7.10 3.4.3 3.5.0 3.6.0 3.7.0

# Make sure that they are all there (they should all have a * next to them)
pyenv versions
```

Once your Python interpreters are installed, you need set up a virtualenv and install tox.

```sh
python -m venv .venv
source .venv/bin/activate
pip install tox
```

Now that everything is installed and set up, you just need one command to run all of the tests against all of our defined Python versions:

```sh
tox
```

Assuming all goes well, you should see a result akin to

```sh
  py27: commands succeeded
  py34: commands succeeded
  py35: commands succeeded
  py36: commands succeeded
  py37: commands succeeded
  pypy: commands succeeded
  pypy3: commands succeeded
  congratulations :)
```

If you run in to an issue with running detox, make sure that you have the latest version of `pip` as there are [some issues](https://github.com/yyuu/pyenv/issues/531) with `pyenv` and older versions of `pip`.

## Contributing

If you would like to contribute to this project, you will need to use [git flow](https://github.com/nvie/gitflow). This way, any and all changes happen on the development branch and not on the master branch. As such, after you have git-flow-ified your `zoomus` git repo, create a pull request for your branch, and we'll take it from there.
