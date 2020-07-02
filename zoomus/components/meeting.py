"""Zoom.us REST API Python Client"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base
import json
import ast


class MeetingComponent(base.BaseComponent):
    """Component dealing with all meeting related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, "host_id")
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/meeting/list", params=kwargs)

    def create(self, **kwargs):
        util.require_keys(kwargs, ["host_id", "topic", "type"])
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/meeting/create", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/meeting/update", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/meeting/delete", params=kwargs)

    def end(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/meeting/end", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/meeting/get", params=kwargs)

class MeetingComponentV2(base.BaseComponent):
    def list(self, **kwargs):
        util.require_keys(kwargs, "user_id")
        return self.get_request(
            "/users/{}/meetings".format(kwargs.get("user_id")), params=kwargs
        )

    def create(self, **kwargs):
        util.require_keys(kwargs, "user_id")
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request(
            "/users/{}/meetings".format(kwargs.get("user_id")), data=kwargs
        )

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request("/meetings/{}".format(kwargs.get("id")), params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, "id")
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.patch_request("/meetings/{}".format(kwargs.get("id")), data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.delete_request(
            "/meetings/{}".format(kwargs.get("id")), params=kwargs
        )

    def register(self, **kwargs):
        util.require_keys(kwargs, ["id", "email", "first_name", "last_name", "phone"])
        
        params={
            "email": kwargs["email"],
            "first_name": kwargs["first_name"],
            "last_name": kwargs["last_name"],
            "custom_questions": [
                {
                    "title": "Phone Number",
                    "value": kwargs["phone"]
                }
            ]
        }

        if "city" in kwargs:
            params["city"] = kwargs["city"]

        return self.post_request(
            "/meetings/{}/registrants".format(kwargs.get("id")), data=params
        )
    
    def approve(self, **kwargs):
        util.require_keys(kwargs, ["id", "email", "userid"])
        params = {
            "action": "approve",
            "registrants": [
                {
                    "id": kwargs["userid"],
                    "email": kwargs["email"]
                }
            ]
        }
        return self.put_request(
            "/meetings/{}/registrants/status".format(kwargs.get("id")), data=params
        )

    def get_registration_questions(self, **kwargs):
        util.require_keys(kwargs, ["id"])
        return self.get_request(
            "/meetings/{}/registrants/questions".format(kwargs.get("id"))
        )