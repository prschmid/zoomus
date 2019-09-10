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
    suite.addTest(unittest.makeSuite(UpcomingV1TestCase))
    return suite


class UpcomingV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    def test_can_upcoming(self):
        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            self.component.upcoming(host_id="ID")

            mock_post_request.assert_called_with(
                "/webinar/list/registration", params={"host_id": "ID"}
            )

    def test_requires_host_id(self):
        with self.assertRaises(ValueError) as context:
            self.component.upcoming()
            self.assertEqual(context.exception.message, "'host_id' must be set")

    def test_does_convert_startime_to_str_if_datetime(self):

        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            start_time = datetime.datetime.utcnow()
            self.component.upcoming(
                host_id="ID", topic="TOPIC", type="TYPE", start_time=start_time
            )

            mock_post_request.assert_called_with(
                "/webinar/list/registration",
                params={
                    "host_id": "ID",
                    "topic": "TOPIC",
                    "type": "TYPE",
                    "start_time": util.date_to_str(start_time),
                },
            )


if __name__ == "__main__":
    unittest.main()
