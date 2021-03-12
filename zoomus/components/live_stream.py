from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class LiveStreamComponentV2(base.BaseComponent):
    def update(self, **kwargs):
        """
        Use this API to update the meeting's stream information.
        Expects:
        - meeting_id: int
        - stream_url: string (URL)
        - stream_key: string
        - page_url: string (URL)
        """
        util.require_keys(kwargs, "meeting_id")
        return self.patch_request(
            "/meetings/{}/livestream".format(kwargs.get("meeting_id")), data=kwargs
        )

    def update_status(self, **kwargs):
        """
        Use this API to update the status of a meeting's live stream.
        Expects:
        - meeting_id: int
        - action (start|stop)
        - settings: dict
        """
        util.require_keys(kwargs, "meeting_id")
        return self.patch_request(
            "/meetings/{}/livestream/status".format(kwargs.get("meeting_id")),
            data=kwargs,
        )
