import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateV1TestCase))
    return suite


class CreateV1TestCase(unittest.TestCase):
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
    def test_can_create(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinar/create?host_id=ID&topic=TOPIC&api_key=KEY&api_secret=SECRET",
        )
        self.component.create(host_id="ID", topic="TOPIC")

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.create()

    def test_requires_topic(self):
        with self.assertRaisesRegexp(ValueError, "'topic' must be set"):
            self.component.create(host_id="ID")

    @responses.activate
    def test_does_convert_startime_to_str_if_datetime(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinar/create?host_id=ID&topic=TOPIC&start_time=1969-01-01T01%3A01%3A00Z"
            "&api_key=KEY&api_secret=SECRET",
        )
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        self.component.create(host_id="ID", topic="TOPIC", start_time=start_time)


class CreateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_create(self):
        responses.add(responses.POST, "http://foo.com/users/42/webinars?user_id=42")
        self.component.create(user_id="42")

    def test_requires_user_id(self):
        with self.assertRaisesRegexp(ValueError, "'user_id' must be set"):
            self.component.create()


if __name__ == "__main__":
    unittest.main()
