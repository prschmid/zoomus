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
    suite.addTest(unittest.makeSuite(GetUserReportV1TestCase))
    return suite


class GetUserReportV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    def test_can_get_user_report(self):
        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            start_time = datetime.datetime.utcnow()
            end_time = datetime.datetime.utcnow()
            self.component.get_user_report(start_time=start_time, end_time=end_time)

            mock_post_request.assert_called_with(
                "/report/getuserreport",
                params={
                    "from": util.date_to_str(start_time),
                    "to": util.date_to_str(end_time),
                },
            )

    def test_requires_start_time(self):
        with self.assertRaises(ValueError) as context:
            self.component.get_user_report()
            self.assertEqual(context.exception.message, "'start_time' must be set")

    def test_requires_end_time(self):
        with self.assertRaises(ValueError) as context:
            self.component.get_user_report(start_time=datetime.datetime.utcnow())
            self.assertEqual(context.exception.message, "'end_time' must be set")

    def test_does_convert_start_time_to_str_if_datetime(self):

        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            start_time = datetime.datetime.utcnow()
            end_time = datetime.datetime.utcnow()

            self.component.get_user_report(start_time=start_time, end_time=end_time)

            mock_post_request.assert_called_with(
                "/report/getuserreport",
                params={
                    "from": util.date_to_str(start_time),
                    "to": util.date_to_str(end_time),
                },
            )


class GetUserReportV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_get_user_report(self, mock_get_request):
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        self.component.get_user_report(
            user_id="ID", start_time=start_time, end_time=end_time
        )

        mock_get_request.assert_called_with(
            "/report/users/ID/meetings",
            params={
                "user_id": "ID",
                "from": util.date_to_str(start_time),
                "to": util.date_to_str(end_time),
            },
        )

    def test_requires_user_id(self):
        with self.assertRaisesRegexp(ValueError, "'user_id' must be set"):
            self.component.get_user_report()

    def test_requires_start_time(self):
        with self.assertRaisesRegexp(ValueError, "'start_time' must be set"):
            self.component.get_user_report(user_id="ID")

    def test_requires_end_time(self):
        with self.assertRaisesRegexp(ValueError, "'end_time' must be set"):
            self.component.get_user_report(
                user_id="ID", start_time=datetime.datetime.utcnow()
            )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_does_convert_start_time_to_str_if_datetime(self, mock_get_request):
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()

        self.component.get_user_report(
            user_id="ID", start_time=start_time, end_time=end_time
        )

        mock_get_request.assert_called_with(
            "/report/users/ID/meetings",
            params={
                "user_id": "ID",
                "from": util.date_to_str(start_time),
                "to": util.date_to_str(end_time),
            },
        )


if __name__ == "__main__":
    unittest.main()
