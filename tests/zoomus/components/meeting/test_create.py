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
        self.component = components.meeting.MeetingComponent(
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
            "http://foo.com/meeting/create?host_id=ID&topic=TOPIC&type=TYPE&api_key=KEY&api_secret=SECRET",
        )
        self.component.create(host_id="ID", topic="TOPIC", type="TYPE")

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.create()

    def test_requires_topic(self):
        with self.assertRaisesRegexp(ValueError, "'topic' must be set"):
            self.component.create(host_id="ID")

    def test_requires_type(self):
        with self.assertRaisesRegexp(ValueError, "'type' must be set"):
            self.component.create(host_id="ID", topic="TOPIC")

    @responses.activate
    def test_does_convert_startime_to_str_if_datetime(self):
        responses.add(
            responses.POST,
            "http://foo.com/meeting/create?host_id=ID&topic=TOPIC&type=TYPE&api_key=KEY&api_secret=SECRET&start_time=2020-01-01T01%3A01%3A00Z",
        )
        start_time = datetime.datetime(2020, 1, 1, 1, 1)
        self.component.create(
            host_id="ID", topic="TOPIC", type="TYPE", start_time=start_time
        )


class CreateV2TestCase(unittest.TestCase):
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
    def test_can_create(self):
        responses.add(
            responses.POST,
            "http://foo.com/users/ID/meetings?user_id=ID&topic=TOPIC&type=TYPE",
        )
        self.component.create(user_id="ID", topic="TOPIC", type="TYPE")

    def test_requires_user_id(self):
        with self.assertRaisesRegexp(ValueError, "'user_id' must be set"):
            self.component.create()

    @responses.activate
    def test_does_convert_startime_to_str_if_datetime(self):
        responses.add(
            responses.POST,
            "http://foo.com/users/ID/meetings?user_id=ID&start_time=2020-01-01T01%3A01%3A00Z",
        )
        start_time = datetime.datetime(2020, 1, 1, 1, 1)
        self.component.create(user_id="ID", start_time=start_time)


if __name__ == "__main__":
    unittest.main()
