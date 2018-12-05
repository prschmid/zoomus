zoomus
==========
![](https://travis-ci.org/actmd/zoomus.svg?branch=master)

[http://github.com/actmd/zoomus](http://github.com/actmd/zoomus)

Python wrapper around the [Zoom.us](http://zoom.us) REST API.

This work is heavily inspired by the Ruby GEM of the same name, [Zoomus](https://github.com/mllocs/zoomus)

Installation
------------

### The easy way

```sh
pip install zoomus
```

### The developer way

```sh
git clone git@github.com:actmd/zoomus.git
cd zoomus
python setup.py install
```

Compatability
-------------

Zoomus has been tested for Python 2.6, 3.2, 3.3, 3.4, and pypy using [Travis CI](https://travis-ci.org/actmd/zoomus)

Example Usage
-------------

### Create the client

```python
from zoomus import ZoomClient

client = ZoomClient('API_KEY', 'API_SECRET')

for user in json.loads(client.user.list())['users']:
    user_id = user['id']
    print client.meeting.list('host_id': user_id)
```

### Using with a manage context

```python
with ZoomClient('API_KEY', 'API_SECRET') as client:
    users = client.users.list()
    ...
```


Available methods
-----------------

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


Running the Tests
-----------------

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

If you don't trust our Travis CI badge above, you can run all of the tests across multiple python versions by using [pyenv](https://github.com/yyuu/pyenv) and [detox](https://pypi.python.org/pypi/detox). A good writeup for what you need to do to set this up can be found [here](http://blog.pinaxproject.com/2015/12/08/how-test-against-multiple-python-versions-parallel/).

Note: If you are using OS X and installed pyenv with brew, make sure to follow [these instructions](https://github.com/yyuu/pyenv#homebrew-on-mac-os-x) as well.

You'll want to make sure that you have all of the different python versions are installed so that they can be tested:

```sh
# Install the versions
pyenv install 2.7.10
pyenv install 3.3.6
pyenv install 3.4.3
pyenv install 3.5.0

# Set all these to be global versions
pyenv global system 2.7.10 3.3.6 3.4.3 3.5.0

# Make sure that they are all there (they should all have a * next to them)
pyenv versions
```

Once you get everything installed, you can run the tests across the different versions as follows.

```sh
detox
```

Note this assumes that you have detox installed globally.

Assuming all goes well, you should see a result akin to

```sh
py27-1.7: commands succeeded
py27-1.8: commands succeeded
py27-1.9: commands succeeded
py27-master: commands succeeded
py33-1.7: commands succeeded
py33-1.8: commands succeeded
py34-1.7: commands succeeded
py34-1.8: commands succeeded
py34-1.9: commands succeeded
py34-master: commands succeeded
py35-1.8: commands succeeded
py35-1.9: commands succeeded
py35-master: commands succeeded
congratulations :)
```

If you run in to an issue with running detox, make sure that you have the latest version of pip as there are [some issues](https://github.com/yyuu/pyenv/issues/531) with pyenv and older versions of pip.

Contributing
------------

If you would like to contribute to this project, you will need to use [git flow](https://github.com/nvie/gitflow). This way, any and all changes happen on the development branch and not on the master branch. As such, after you have git-flow-ified your zoomus git repo, create a pull request for your branch, and we'll take it from there.
