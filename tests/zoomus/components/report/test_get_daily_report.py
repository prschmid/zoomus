import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetDailyReportV1TestCase))
    suite.addTest(unittest.makeSuite(GetDailyReportV2TestCase))
    return suite


class GetDailyReportV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponent(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_get_daily_report(self):
        responses.add(
            responses.POST,
            "http://foo.com/report/getdailyreport?month=01&year=2020"
            "&api_key=CLIENT_ID&api_secret=SECRET",
        )

        self.component.get_daily_report(month="01", year="2020")

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


class GetDailyReportV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponentV2(
            base_uri="http://foo.com", config={"client_id": "CLIENT_ID", "client_secret": "SECRET"}
        )

    @responses.activate
    def test_can_get_daily_report(self):
        responses.add(responses.GET, "http://foo.com/report/daily?month=01&year=2020")
        self.component.get_daily_report(month="01", year="2020")

    def test_requires_month(self):
        with self.assertRaisesRegex(ValueError, "'month' must be set"):
            self.component.get_daily_report()

    def test_requires_year(self):
        with self.assertRaisesRegex(ValueError, "'year' must be set"):
            self.component.get_daily_report(
                month=datetime.datetime.now().strftime("%Y")
            )


if __name__ == "__main__":
    unittest.main()
