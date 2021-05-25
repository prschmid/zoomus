**Zoomus 1.1.5**
================

|Build Status|

Python wrapper around the Zoom.us REST API v1 and v2. This work is heavily inspired by the Ruby GEM of the same name, Zoomus

.. |Build Status| raw:: html

    <a href="https://travis-ci.org/github/prschmid/zoomus">
        <img src="https://travis-ci.org/prschmid/zoomus.svg?branch=develop"/>
    </a>


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Contents
========

1. :ref:`Installation`.
2. :ref:`Usage`.
3. :ref:`Create user using API V2`.
4. :ref:`Zoom User Methods provided by zoomus client`
5. :ref:`Zoom Meeting Methods provided by zoomus client`.
6. :ref:`Zoom Report Methods provided by zoomus client`.
7. :ref:`Zoom Webinar Methods provided by zoomus client`.
8. :ref:`Zoom Phone Methods provided by zoomus client`.
9. :ref:`Zoom Groups Methods provided by zoomus client`.
10. :ref:`Running the Tests`.
11. :ref:`Contributing`.

.. _Installation:

**Installation**
----------------

To install zoomus::

    $ pip install zoomus

.. _Usage:

**Usage**
---------

Initialize client with API_KEY and API_SECRET
*********************************************

As Zoom's default is now the V2 API, the client will default to the V2 version of the API

*For API V2*
############

::

  import json
  from zoomus import ZoomClient

  client = ZoomClient('API_KEY', 'API_SECRET')

*For API V1*
#############

Zoom has yet to officially remove support for the V1 API, and so to use the V1 API one can instantiate a client as follows.

::

  import json
  from zoomus import ZoomClient

  client = ZoomClient('API_KEY', 'API_SECRET', version=1)


*Using with a manage context*
#############################

::

  with ZoomClient('API_KEY', 'API_SECRET') as client:
    user_list_response = client.users.list()


.. _Create user using API V2:

Create user using API V2:
*************************

*Refer Create User* `https://marketplace.zoom.us/docs/api-reference/zoom-api/users/usercreate`

::

  params = {
    "action": "create",
    "user_info": {
      "email": "example@test.com",
      "type": 1,
      "first_name": "Terry",
      "last_name": "Jones"
    }
  }
  resp = client.user.create(**data)
  if resp.status_code == 200:
      print(resp.json())


*Refer Create User Response* `https://marketplace.zoom.us/docs/api-reference/zoom-api/users/usercreate#responses`

Example Response on Success::

  {
    "id": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "type": "integer"
  }


.. _Zoom User Methods provided by zoomus client:

Zoom User Methods provided by zoomus client:
********************************************
*Refer Zoom User API Docs for params info* `https://marketplace.zoom.us/docs/api-reference/zoom-api/users`

::

  client.user.cust_create(...)

  client.user.update(...)*

  client.user.check_email(...)

  client.user.update_email(...)

  client.user.list(...)

  client.user.pending(...)

  client.user.get(...)

  client.user.get_by_email(...)

  client.user.get_settings(...)

  client.user.update_settings(...)


.. _Zoom Meeting Methods provided by zoomus client:

Zoom Meeting Methods provided by zoomus client:
***********************************************
*Refer Zoom Meeting API Docs for params info* `https://marketplace.zoom.us/docs/api-reference/zoom-api/meetings`

::

  client.meeting.get(...)

  client.meeting.end(...)

  client.meeting.create(...)

  client.meeting.delete(...)

  client.meeting.list(...)

  client.meeting.update(...)

  client.meeting.add_registrant(...)

  client.meeting.list_registrants(...)

  client.meeting.update_registrant_status(...)

  client.meeting.update_status(...)


.. _Zoom Report Methods provided by zoomus client:

Zoom Report Methods provided by zoomus client:
**********************************************
*Refer Zoom Report API Docs* `https://marketplace.zoom.us/docs/api-reference/zoom-api/reports`

::

  client.report.get_account_report(...)

  client.report.get_user_report(...)


.. _Zoom Webinar Methods provided by zoomus client:

Zoom Webinar Methods provided by zoomus client:
***********************************************
*Refer Zoom Webinar API Docs for params info* `https://marketplace.zoom.us/docs/api-reference/zoom-api/webinars`

::

  client.webinar.create(...)

  client.webinar.update(...)

  client.webinar.delete(...)

  client.webinar.list(...)

  client.webinar.get(...)

  client.webinar.end(...)

  client.webinar.register(...)

  client.webinar.add_panelists(...)

  client.webinar.list_panelists(...)

  client.webinar.remove_panelists(...)


.. _Zoom Phone Methods provided by zoomus client:

Zoom Phone Methods provided by zoomus client:
*********************************************
*Refer Zoom Phone API Docs for params info* `https://marketplace.zoom.us/docs/api-reference/zoom-api/phone`

::

  client.phone.call_logs(...)

  client.phone.calling_plans(...)

  client.phone.numbers_get(...)

  client.phone.numbers_list(...)

  client.phone.users(...)



.. _Zoom Groups Methods provided by zoomus client:

Zoom Groups Methods provided by zoomus client:
**********************************************
*Refer Zoom Groups API Docs for params info* `https://marketplace.zoom.us/docs/api-reference/zoom-api/groups`

::

  client.group.list(...)

  client.group.create(...)

  client.group.get(...)

  client.group.delete(...)

  client.group.list_members(...)

  client.group.add_members(...)

  client.group.delete_member(...)

Zoom Rooms Methods provided by zoomus client:
**********************************************
*Refer Zoom Rooms API Docs for params info* `https://marketplace.zoom.us/docs/api-reference/zoom-api/rooms/`

::

  client.room.list(...)

  client.room.create(...)

  client.room.get(...)

  client.room.get_settings(...)

  client.room.get_devices(...)

  client.room.delete(...)

  client.room.check_in_or_out(...)

  client.room.update(...)

.. _Running the Tests:

Running the Tests
-----------------

Install the testing requirements

::

  pip install -r requirements-tests.txt

Then run the tests via nose

::

  nosetests

.. _Contributing:

Contributing
------------

Please see the CONTRIBUTING.md for the contribution guidelines for this project.
