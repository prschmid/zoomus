from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class LiveStreamComponentV2(base.BaseComponent):
    """
    Use this API to update the meeting's stream information.
    Expects:
    - meeting_id: int
    - stream_url: string (URL)
    - stream_key: string
    - page_url: string (URL)
    """

    def update(self, **kwargs):
        util.require_keys(kwargs, "meeting_id")
        return self.patch_request(
            "/meetings/{}/livestream".format(kwargs.get("meeting_id")), data=kwargs
        )
