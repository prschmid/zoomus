import unittest

from zoomus import components, util
import responses


class UpdateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.live_stream.LiveStreamComponentV2(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_update(self):
        responses.add(responses.PATCH, "http://foo.com/meetings/42/livestream/status")
        response = self.component.update_status(
            meeting_id="42",
            action="stop",
            settings={"active_speaker_name": False, "display_name": "inc"},
        )
        self.assertEqual(
            response.request.body,
            '{"meeting_id": "42", "action": "stop", "settings": {"active_speaker_name": false, "display_name": "inc"}}',
        )

    @responses.activate
    def test_can_update_wildcard(self):
        responses.add(responses.PATCH, "http://foo.com/meetings/42/livestream/status")

        data = {
            "meeting_id": "42",
            "action": "stop",
            "settings": {"active_speaker_name": False, "display_name": "inc"},
        }

        response = self.component.update_status(**data)
        self.assertEqual(
            response.request.body,
            '{"meeting_id": "42", "action": "stop", "settings": {"active_speaker_name": false, "display_name": "inc"}}',
        )

    def test_requires_meeting_id(self):
        with self.assertRaises(ValueError) as context:
            self.component.update_status()
            self.assertEqual(context.exception.message, "'meeting_id' must be set")

    @responses.activate
    def test_can_update_webinar_livestream(self):
        responses.add(responses.PATCH, "http://foo.com/webinars/42/livestream/status")
        response = self.component.update_webinar_status(
            webinar_id="42",
            action="stop",
            settings={"active_speaker_name": False, "display_name": "inc"},
        )
        self.assertEqual(
            response.request.body,
            '{"webinar_id": "42", "action": "stop", "settings": {"active_speaker_name": false, "display_name": "inc"}}',
        )

    @responses.activate
    def test_can_update_webinar_wildcard(self):
        responses.add(responses.PATCH, "http://foo.com/webinars/42/livestream/status")

        data = {
            "webinar_id": "42",
            "action": "stop",
            "settings": {"active_speaker_name": False, "display_name": "inc"},
        }

        response = self.component.update_webinar_status(**data)
        self.assertEqual(
            response.request.body,
            '{"webinar_id": "42", "action": "stop", "settings": {"active_speaker_name": false, "display_name": "inc"}}',
        )

    def test_requires_webinar_id(self):
        with self.assertRaises(ValueError) as context:
            self.component.update_webinar_status()
            self.assertEqual(context.exception.message, "'webinar_id' must be set")


if __name__ == "__main__":
    unittest.main()
