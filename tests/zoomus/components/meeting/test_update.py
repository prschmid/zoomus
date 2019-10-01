from datetime import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateV1TestCase))
    suite.addTest(unittest.makeSuite(UpdateV2TestCase))
    return suite


class UpdateV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponent(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_update(self):
        responses.add(
            responses.POST,
            "http://foo.com/meeting/update?id=ID&host_id=ID&api_key=KEY&api_secret=SECRET",
        )
        self.component.update(id="ID", host_id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update()

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.update(id="ID")

    @responses.activate
    def test_start_time_gets_transformed(self):
        responses.add(
            responses.POST,
            "http://foo.com/meeting/update?id=ID&host_id=ID&start_time=2020-01-01T01%3A01%3A00Z"
            "&api_key=KEY&api_secret=SECRET",
        )
        start_time = datetime(2020, 1, 1, 1, 1)
        self.component.update(id="ID", host_id="ID", start_time=start_time)


class UpdateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_update(self):
        responses.add(responses.PATCH, "http://foo.com/meetings/42?id=42&foo=bar")
        self.component.update(id="42", foo="bar")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update()

    @responses.activate
    def test_start_time_gets_transformed(self):
        responses.add(
            responses.PATCH,
            "http://foo.com/meetings/42?id=42&start_time=2020-01-01T01%3A01%3A00Z",
        )
        self.component.update(id="42", start_time=datetime(2020, 1, 1, 1, 1))


if __name__ == "__main__":
    unittest.main()
