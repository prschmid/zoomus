import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetV2TestCase))
    return suite


class GetV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.live_stream.LiveStreamComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_get(self):
        responses.add(responses.GET, "http://foo.com/meetings/ID/livestream")
        self.component.get_livestream(meeting_id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.get_livestream()

    @responses.activate
    def test_can_get_webinar(self):
        responses.add(responses.GET, "http://foo.com/webinars/ID/livestream")
        self.component.get_webinar_livestream(webinar_id="ID")

    def test_requires_id_webinar(self):
        with self.assertRaisesRegexp(ValueError, "'webinar_id' must be set"):
            self.component.get_webinar_livestream()


if __name__ == "__main__":
    unittest.main()
