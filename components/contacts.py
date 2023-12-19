"""Zoom.us REST API Python Client -- Contacts component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class ContactsComponentV2(base.BaseComponent):
    def search(self, **kwargs):
        util.require_keys(kwargs, ["search_key"])
        return self.get_request("/contacts", params=kwargs)

    def list_user_contacts(self, **kwargs):
        return self.get_request("/chat/users/me/contacts", params=kwargs)

    def get_user_contact(self, **kwargs):
        util.require_keys(kwargs, ["contact_id"])
        return self.get_request(
            "/chat/users/me/contacts/{}".format(kwargs.get("contact_id")), params=kwargs
        )
