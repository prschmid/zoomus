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

Contributing
------------

If you would like to contribute to this project, you will need to use [git flow](https://github.com/nvie/gitflow). This way, any and all changes happen on the development branch and not on the master branch. As such, after you have git-flow-ified your zoomus git repo, create a pull request for your branch, and we'll take it from there.
