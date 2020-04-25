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
        self.component = components.recording.RecordingComponent(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_list(self):
        responses.add(
            responses.POST,
            "http://foo.com/recording/list?host_id=ID&api_key=KEY&api_secret=SECRET",
        )
        self.component.list(host_id="ID")

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.list()

    @responses.activate
    def test_does_convert_startime_to_str_if_datetime(self):
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        end_time = datetime.datetime(2020, 1, 1, 1, 1)
        responses.add(
            responses.POST,
            "http://foo.com/recording/list?host_id=42&meeting_number=111&api_key=KEY&api_secret=SECRET"
            "&from=1969-01-01T01%3A01%3A00Z&to=2020-01-01T01%3A01%3A00Z",
        )
        self.component.list(
            host_id="42", start=start_time, end=end_time, meeting_number="111"
        )


class ListV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.recording.RecordingComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_list(self):
        responses.add(responses.GET, "http://foo.com/users/42/recordings?user_id=42")
        self.component.list(user_id="42")

    def test_requires_user_id(self):
        with self.assertRaisesRegexp(ValueError, "'user_id' must be set"):
            self.component.list()

    @responses.activate
    def test_does_convert_startime_to_str_if_datetime(self):
        responses.add(
            responses.GET,
            "http://foo.com/users/42/recordings?user_id=42&meeting_number=111"
            "&from=1969-01-01T01%3A01%3A00Z&to=2020-01-01T01%3A01%3A00Z",
        )
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        end_time = datetime.datetime(2020, 1, 1, 1, 1)
        self.component.list(
            user_id="42", start=start_time, end=end_time, meeting_number="111"
        )


if __name__ == "__main__":
    unittest.main()
