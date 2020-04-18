"""Zoom.us REST API Python Client"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class MetricComponentV2(base.BaseComponent):
    def list_meetings(self, **kwargs):
        return self.get_request("/metrics/meetings", params=kwargs,)

    def get_meeting(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        kwargs["meeting_id"] = util.encode_uuid(kwargs.get("meeting_id"))
        return self.get_request(
            "/metrics/meetings/{}".format(kwargs.get("meeting_id")), params=kwargs
        )

    def list_participants(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        kwargs["meeting_id"] = util.encode_uuid(kwargs.get("meeting_id"))
        return self.get_request(
            "/metrics/meetings/{}/participants".format(kwargs.get("meeting_id")),
            params=kwargs,
        )

    def get_participant_qos(self, **kwargs):
        util.require_keys(kwargs, ("meeting_id", "participant_id"))
        kwargs["meeting_id"] = util.encode_uuid(kwargs.get("meeting_id"))
        return self.get_request(
            "/metrics/meetings/{}/participants/{}/qos".format(
                kwargs.get("meeting_id"), kwargs.get("participant_id")
            ),
            params=kwargs,
        )

    def list_participants_qos(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        kwargs["meeting_id"] = util.encode_uuid(kwargs.get("meeting_id"))
        return self.get_request(
            "/metrics/meetings/{}/participants/qos".format(kwargs.get("meeting_id")),
            params=kwargs,
        )
