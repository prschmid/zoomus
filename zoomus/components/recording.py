"""Zoom.us REST API Python Client -- Recording component"""
from zoomus import util
from zoomus.components import base


class RecordingComponent(base.BaseComponent):
    """Component dealing with all recording related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, "host_id")
        start = kwargs.pop("start", None)
        if start:
            kwargs["from"] = util.date_to_str(start)
        end = kwargs.pop("end", None)
        if end:
            kwargs["to"] = util.date_to_str(end)
        return self.post_request("/recording/list", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, ["meeting_id"])
        return self.post_request("/recording/delete", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, ["meeting_id"])
        return self.post_request("/recording/get", params=kwargs)


class RecordingComponentV2(base.BaseComponent):
    """Component dealing with all recording related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, "user_id")
        start = kwargs.pop("start", None)
        if start:
            kwargs["from"] = util.date_to_str(start)
        end = kwargs.pop("end", None)
        if end:
            kwargs["to"] = util.date_to_str(end)
        return self.get_request(
            "/users/{}/recordings".format(kwargs.get("user_id")), params=kwargs
        )

    def get(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        return self.get_request(
            "/meetings/{}/recordings".format(kwargs.get("meeting_id")), params=kwargs
        )

    def delete(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        return self.delete_request(
            "/meetings/{}/recordings".format(kwargs.get("meeting_id")), params=kwargs
        )
