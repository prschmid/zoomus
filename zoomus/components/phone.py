"""Zoom.us REST API Python Client -- Phone component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class PhoneComponentV2(base.BaseComponent):
    def numbers_list(self, **kwargs):
        return self.get_request("/phone/numbers", params=kwargs)

    def numbers_get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request(
            "/phone/numbers/{}".format(kwargs.get("id")), params=kwargs
        )

    def call_logs(self, **kwargs):
        return self.get_request("/phone/call_logs", params=kwargs)

    def calling_plans(self, **kwargs):
        return self.get_request("/phone/calling_plans", params=kwargs)

    def users(self, **kwargs):
        return self.get_request("/phone/users", params=kwargs)
