"""Zoom.us REST API Python Client"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class PastMeetingComponentV2(base.BaseComponent):
    def list(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        kwargs["meeting_id"] = util.encode_uuid(kwargs.get("meeting_id"))
        return self.get_request(
            "/past_meetings/{}/instances".format(kwargs.get("meeting_id")),
            params=kwargs,
        )

    def get(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        kwargs["meeting_id"] = util.encode_uuid(kwargs.get("meeting_id"))
        return self.get_request(
            "/past_meetings/{}".format(kwargs.get("meeting_id")), params=kwargs
        )

    def get_participants(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        kwargs["meeting_id"] = util.encode_uuid(kwargs.get("meeting_id"))
        return self.get_request(
            "/past_meetings/{}/participants".format(kwargs.get("meeting_id")),
            params=kwargs,
        )
