import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateV2TestCase))
    return suite


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
        responses.add(responses.PATCH, "http://foo.com/meetings/42/livestream")
        response = self.component.update(
            meeting_id="42", stream_url="https://foo.bar", stream_key="12345"
        )
        self.assertEqual(
            response.request.body,
            '{"meeting_id": "42", "stream_url": "https://foo.bar", "stream_key": "12345"}',
        )

    @responses.activate
    def test_can_update_wildcard(self):
        responses.add(responses.PATCH, "http://foo.com/meetings/42/livestream")

        data = {
            "meeting_id": "42",
            "stream_url": "https://foo.bar",
            "stream_key": "12345",
        }

        response = self.component.update(**data)
        self.assertEqual(
            response.request.body,
            '{"meeting_id": "42", "stream_url": "https://foo.bar", "stream_key": "12345"}',
        )

    def test_requires_meeting_id(self):
        with self.assertRaises(ValueError) as context:
            self.component.update()
            self.assertEqual(context.exception.message, "'meeting_id' must be set")


if __name__ == "__main__":
    unittest.main()
