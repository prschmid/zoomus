from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class LiveStreamStatusComponentV2(base.BaseComponent):
    """
    Use this API to update the status of a meeting's live stream.
    Expects:
    - meeting_id: int
    - action (start|stop)
    - settings: dict
    """

    def update(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        return self.patch_request(
            "/meetings/{}/livestream/status".format(kwargs.get("meeting_id")),
            data=kwargs,
        )
