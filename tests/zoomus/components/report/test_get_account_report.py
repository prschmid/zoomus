import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetAccountReportV1TestCase))
    return suite


class GetAccountReportV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponent(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_get_account_report(self):
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        end_time = datetime.datetime(2020, 1, 1, 1, 1)
        responses.add(
            responses.POST,
            "http://foo.com/report/getaccountreport?from=1969-01-01T01%3A01%3A00Z&to=2020-01-01T01%3A01%3A00Z"
            "&api_key=KEY&api_secret=SECRET",
        )
        self.component.get_account_report(start_time=start_time, end_time=end_time)

    def test_requires_start_time(self):
        with self.assertRaisesRegexp(ValueError, "'start_time' must be set"):
            self.component.get_account_report()

    def test_requires_end_time(self):
        with self.assertRaisesRegexp(ValueError, "'end_time' must be set"):
            self.component.get_account_report(start_time=datetime.datetime.utcnow())


class GetAccountReportV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_get_account_report(self):
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        end_time = datetime.datetime(2020, 1, 1, 1, 1)
        responses.add(
            responses.GET,
            "http://foo.com/report/users?from=1969-01-01T01%3A01%3A00Z&to=2020-01-01T01%3A01%3A00Z",
        )
        self.component.get_account_report(start_time=start_time, end_time=end_time)

    def test_requires_start_time(self):
        with self.assertRaisesRegexp(ValueError, "'start_time' must be set"):
            self.component.get_account_report()

    def test_requires_end_time(self):
        with self.assertRaisesRegexp(ValueError, "'end_time' must be set"):
            self.component.get_account_report(start_time=datetime.datetime.utcnow())


if __name__ == "__main__":
    unittest.main()
