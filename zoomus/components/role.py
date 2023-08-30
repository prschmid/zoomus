"""Zoom.us REST API Python Client"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class RoleComponentV2(base.BaseComponent):
    def assign(self, **kwargs):
        util.require_keys(kwargs, ["id", "members"])

        return self.post_request(
            "/roles/{}/members".format(kwargs.pop("id")), data=kwargs
        )

    def create(self, **kwargs):
        util.require_keys(kwargs, ["name", "description", "privileges"])

        try:
            util.require_keys(kwargs, "type")
        except ValueError:
            kwargs["type"] = "common"

        return self.post_request("/roles", data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")

        return self.delete_request("/roles/{}".format(kwargs.pop("id")))

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")

        return self.get_request("/roles/{}/".format(kwargs.pop("id")))

    def get_members(self, **kwargs):
        util.require_keys(kwargs, "id")

        return self.get_request(
            "/roles/{}/members".format(kwargs.pop("id")), params=kwargs
        )

    def list(self, **kwargs):
        return self.get_request("/roles", params=kwargs)

    def unassign(self, **kwargs):
        util.require_keys(kwargs, ["id", "member"])

        return self.delete_request(
            "/roles/{roleId}/members/{memberId}".format(
                roleId=kwargs.pop("id"), memberId=kwargs["member"]
            )
        )

    def update(self, **kwargs):
        util.require_keys(kwargs, ["id", "name", "description", "privileges"])

        return self.patch_request("/roles/{}".format(kwargs.pop("id")), data=kwargs)
