"""Zoom.us REST API Python Client -- Room component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class RoomComponentV2(base.BaseComponent):
    def create(self, **kwargs):
        util.require_keys(kwargs, ["name", "type"])
        return self.post_request("/rooms", data=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request("/rooms/{}".format(kwargs.get("id")), params=kwargs)

    def get_devices(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request(
            "/rooms/{}/devices".format(kwargs.get("id")), params=kwargs
        )

    def get_settings(self, **kwargs):
        util.require_keys(kwargs, ["id", "setting_type"])
        return self.get_request(
            "/rooms/{}/settings".format(kwargs.pop("id")), params=kwargs
        )

    def list(self, **kwargs):
        return self.get_request("/rooms/", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.patch_request("/rooms/{}".format(kwargs.get("id")), data=kwargs)

    def check_in_or_out(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.patch_request(
            "/rooms/{}/events".format(kwargs.get("id")), data=kwargs
        )

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.delete_request("/rooms/{}".format(kwargs.get("id")), params=kwargs)
