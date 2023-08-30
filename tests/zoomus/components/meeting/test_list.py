import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ListV1TestCase))
    suite.addTest(unittest.makeSuite(ListV2TestCase))
    return suite


class ListV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponent(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_list(self):
        responses.add(
            responses.POST,
            "http://foo.com/meeting/list?host_id=ID&api_key=CLIENT_ID&api_secret=SECRET",
        )
        self.component.list(host_id="ID")

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.list()

    @responses.activate
    def test_does_convert_startime_to_str_if_datetime(self):
        responses.add(
            responses.POST,
            "http://foo.com/meeting/list?host_id=ID&topic=TOPIC&type=TYPE&start_time=2020-01-01T01%3A01%3A00Z"
            "&api_key=CLIENT_ID&api_secret=SECRET",
        )
        start_time = datetime.datetime(2020, 1, 1, 1, 1)
        self.component.list(
            host_id="ID", topic="TOPIC", type="TYPE", start_time=start_time
        )


class ListV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponentV2(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_list(self):
        responses.add(responses.GET, "http://foo.com/users/ID/meetings?user_id=ID")
        self.component.list(user_id="ID")

    def test_requires_user_id(self):
        with self.assertRaisesRegexp(ValueError, "'user_id' must be set"):
            self.component.list()


if __name__ == "__main__":
    unittest.main()
