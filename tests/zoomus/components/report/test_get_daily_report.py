import datetime
import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetDailyReportV1TestCase))
    return suite


class GetDailyReportV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    def test_can_get_Daily_report(self):
        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            month = datetime.datetime.now().strftime("%m")
            year = datetime.datetime.now().strftime("%Y")

            self.component.get_daily_report(month=month, year=year)

            mock_post_request.assert_called_with(
                "/report/getdailyreport", params={"month": month, "year": year},
            )

    def test_requires_month(self):
        with self.assertRaises(ValueError) as context:
            self.component.get_daily_report()
            self.assertEqual(context.exception.message, "'month' must be set")

    def test_requires_year(self):
        with self.assertRaises(ValueError) as context:
            self.component.get_daily_report(
                month=datetime.datetime.now().strftime("%m")
            )
            self.assertEqual(context.exception.message, "'year' must be set")

    def test_does_convert_start_time_to_str_if_datetime(self):

        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            month = datetime.datetime.now().strftime("%m")
            year = datetime.datetime.now().strftime("%Y")

            self.component.get_daily_report(month=month, year=year)

            mock_post_request.assert_called_with(
                "/report/getdailyreport", params={"month": month, "year": year},
            )


class GetDailyReportV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_get_Daily_report(self, mock_get_request):

        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%Y")

        self.component.get_daily_report(month=month, year=year)

        mock_get_request.assert_called_with(
            "/report/daily", params={"month": month, "year": year},
        )

    def test_requires_month(self):
        with self.assertRaisesRegex(ValueError, "'month' must be set"):
            self.component.get_daily_report()

    def test_requires_year(self):
        with self.assertRaisesRegex(ValueError, "'year' must be set"):
            self.component.get_daily_report(
                month=datetime.datetime.now().strftime("%Y")
            )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_does_convert_start_time_to_str_if_datetime(self, mock_get_request):

        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%Y")

        self.component.get_daily_report(month=month, year=year)

        mock_get_request.assert_called_with(
            "/report/daily", params={"month": month, "year": year},
        )


if __name__ == "__main__":
    unittest.main()
