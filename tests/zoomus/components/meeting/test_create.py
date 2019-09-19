import datetime
import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components, util


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateV1TestCase))
    return suite


class CreateV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    def test_can_create(self):
        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            self.component.create(host_id="ID", topic="TOPIC", type="TYPE")

            mock_post_request.assert_called_with(
                "/meeting/create",
                params={"host_id": "ID", "topic": "TOPIC", "type": "TYPE"},
            )

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.create()

    def test_requires_topic(self):
        with self.assertRaisesRegexp(ValueError, "'topic' must be set"):
            self.component.create(host_id="ID")

    def test_requires_type(self):
        with self.assertRaisesRegexp(ValueError, "'type' must be set"):
            self.component.create(host_id="ID", topic="TOPIC")

    @patch.object(components.base.BaseComponent, "post_request", return_value=True)
    def test_does_convert_startime_to_str_if_datetime(self, mock_post_request):
        start_time = datetime.datetime.utcnow()
        self.component.create(
            host_id="ID", topic="TOPIC", type="TYPE", start_time=start_time
        )

        mock_post_request.assert_called_with(
            "/meeting/create",
            params={
                "host_id": "ID",
                "topic": "TOPIC",
                "type": "TYPE",
                "start_time": util.date_to_str(start_time),
            },
        )


class CreateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "post_request", return_value=True)
    def test_can_create(self, mock_post_request):
        self.component.create(user_id="ID", topic="TOPIC", type="TYPE")

        mock_post_request.assert_called_with(
            "/users/ID/meetings",
            params={"user_id": "ID", "topic": "TOPIC", "type": "TYPE"},
        )

    def test_requires_user_id(self):
        with self.assertRaisesRegexp(ValueError, "'user_id' must be set"):
            self.component.create()

    @patch.object(components.base.BaseComponent, "post_request", return_value=True)
    def test_does_convert_startime_to_str_if_datetime(self, mock_post_request):
        start_time = datetime.datetime.utcnow()
        self.component.create(user_id="ID", start_time=start_time)

        mock_post_request.assert_called_with(
            "/users/ID/meetings",
            params={"user_id": "ID", "start_time": util.date_to_str(start_time)},
        )


if __name__ == "__main__":
    unittest.main()
