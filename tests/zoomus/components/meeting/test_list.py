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
    suite.addTest(unittest.makeSuite(ListV1TestCase))
    suite.addTest(unittest.makeSuite(ListV2TestCase))
    return suite


class ListV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    def test_can_list(self):
        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            self.component.list(host_id="ID")

            mock_post_request.assert_called_with(
                "/meeting/list", params={"host_id": "ID"}
            )

    def test_requires_host_id(self):
        with self.assertRaises(ValueError) as context:
            self.component.list()
            self.assertEqual(context.exception.message, "'host_id' must be set")

    def test_does_convert_startime_to_str_if_datetime(self):

        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            start_time = datetime.datetime.utcnow()
            self.component.list(
                host_id="ID", topic="TOPIC", type="TYPE", start_time=start_time
            )

            mock_post_request.assert_called_with(
                "/meeting/list",
                params={
                    "host_id": "ID",
                    "topic": "TOPIC",
                    "type": "TYPE",
                    "start_time": util.date_to_str(start_time),
                },
            )


class ListV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_list(self, mock_get_request):
        self.component.list(user_id="ID")

        mock_get_request.assert_called_with(
            "/users/ID/meetings", params={"user_id": "ID"}
        )

    def test_requires_user_id(self):
        with self.assertRaisesRegexp(ValueError, "'user_id' must be set"):
            self.component.list()


if __name__ == "__main__":
    unittest.main()
