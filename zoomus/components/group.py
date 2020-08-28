"""Zoom.us REST API Python Client"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class GroupComponentV2(base.BaseComponent):
    def list(self, **kwargs):
        return self.get_request("/groups", params=kwargs)

    def create(self, **kwargs):
        util.require_keys(kwargs, "name")
        return self.post_request("/groups", data=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request("/groups/{}".format(kwargs.get("id")), params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.delete_request("/groups/{}".format(kwargs.get("id")), params=kwargs)

    def list_members(self, **kwargs):
        util.require_keys(kwargs, "groupid")
        return self.get_request(
            "/groups/{}/members".format(kwargs.get("groupid")), params=kwargs
        )

    def add_members(self, **kwargs):
        util.require_keys(kwargs, ["groupid", "members"])
        return self.post_request(
            "/groups/{}/members".format(kwargs.get("groupid")), data=kwargs
        )

    def delete_member(self, **kwargs):
        util.require_keys(kwargs, ["groupid", "memberid"])
        return self.delete_request(
            "/groups/{}/members/{}".format(
                kwargs.get("groupid"), kwargs.get("memberid")
            ),
            params=kwargs,
        )
