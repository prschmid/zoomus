import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpcomingV1TestCase))
    return suite


class UpcomingV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponent(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_upcoming(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinar/list/registration?host_id=ID&api_key=KEY&api_secret=SECRET",
        )
        self.component.upcoming(host_id="ID")

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.upcoming()

    @responses.activate
    def test_does_convert_startime_to_str_if_datetime(self):
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        responses.add(
            responses.POST,
            "http://foo.com/webinar/list/registration?host_id=ID&topic=TOPIC&type=TYPE"
            "&start_time=1969-01-01T01%3A01%3A00Z&api_key=KEY&api_secret=SECRET",
        )
        self.component.upcoming(
            host_id="ID", topic="TOPIC", type="TYPE", start_time=start_time
        )


if __name__ == "__main__":
    unittest.main()
