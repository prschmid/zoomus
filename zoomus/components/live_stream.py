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

        Response content sample:
        ```json
        {
        "page_url": "https://example.com/livestream/123",
        "stream_key": "contact-it@example.com",
        "stream_url": "https://example.com/livestream"
        }
        ```
        Returns:
        requests.Response: The response object
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

        Response content sample:
        ```json
        {
        "action": "start",
        "settings": {
            "active_speaker_name": true,
            "display_name": "Jill Chill"
        }
        ```

        Returns:
        requests.Response: The response object
        """
        util.require_keys(kwargs, "meeting_id")
        return self.patch_request(
            "/meetings/{}/livestream/status".format(kwargs.get("meeting_id")),
            data=kwargs,
        )

    def get_livestream(self, **kwargs):
        """
        Get the meeting's live stream details
        Expects:
        - meeting_id: int

        Response content sample:
        ```json
        {
        "page_url": "https://example.com/livestream/123",
        "stream_key": "contact-ic@example.com",
        "stream_url": "https://example.com/livestream"
        }
        ```

        Returns:
        requests.Response: The response object
        """
        util.require_keys(kwargs, "meeting_id")
        return self.get_request(
            "/meetings/{}/livestream".format(kwargs.get("meeting_id")), params=kwargs
        )

    def update_webinar(self, **kwargs):
        """
        Use this API to update the webinar's stream information.
        Expects:
        - webinar_id: int
        - stream_url: string (URL)
        - stream_key: string
        - page_url: string (URL)

        Response content sample:
        ```json
        {
        "page_url": "https://example.com/livestream/123",
        "stream_key": "contact-it@example.com",
        "stream_url": "https://example.com/livestream"
        }
        ```
        Returns:
        requests.Response: The response object
        """
        util.require_keys(kwargs, "webinar_id")
        return self.patch_request(
            "/webinars/{}/livestream".format(kwargs.get("webinar_id")), data=kwargs
        )

    def update_webinar_status(self, **kwargs):
        """
        Use this API to update the status of a webinar's live stream.
        Expects:
        - webinar_id: int
        - action (start|stop)
        - settings: dict

        Response content sample:
        ```json
        {
        "action": "start",
        "settings": {
            "active_speaker_name": true,
            "display_name": "Jill Chill"
        }
        ```

        Returns:
        requests.Response: The response object
        """
        util.require_keys(kwargs, "webinar_id")
        return self.patch_request(
            "/webinars/{}/livestream/status".format(kwargs.get("webinar_id")),
            data=kwargs,
        )

    def get_webinar_livestream(self, **kwargs):
        """Get the webinar's live stream details
        Expects:
        - webinar_id: int
        Response content sample:
        ```json
        {
        "page_url": "https://example.com/livestream/123",
        "stream_key": "contact-ic@example.com",
        "stream_url": "https://example.com/livestream"
        }
        ```

        Returns:
        requests.Response: The response object
        """
        util.require_keys(kwargs, "webinar_id")
        return self.get_request(
            "/webinars/{}/livestream".format(kwargs.get("webinar_id")), params=kwargs
        )
