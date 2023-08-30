import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetUserReportV1TestCase))
    suite.addTest(unittest.makeSuite(GetUserReportV2TestCase))
    return suite


class GetUserReportV1TestCase(unittest.TestCase):
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
    def test_can_get_user_report(self):
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        end_time = datetime.datetime(2020, 1, 1, 1, 1)
        responses.add(
            responses.POST,
            "http://foo.com/report/getuserreport?from=1969-01-01T01%3A01%3A00Z&to=2020-01-01T01%3A01%3A00Z"
            "&api_key=CLIENT_ID&api_secret=SECRET",
        )
        self.component.get_user_report(start_time=start_time, end_time=end_time)

    def test_requires_start_time(self):
        with self.assertRaisesRegexp(ValueError, "'start_time' must be set"):
            self.component.get_user_report()

    def test_requires_end_time(self):
        with self.assertRaisesRegexp(ValueError, "'end_time' must be set"):
            self.component.get_user_report(start_time=datetime.datetime.utcnow())


class GetUserReportV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.report.ReportComponentV2(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_get_user_report(self):
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        end_time = datetime.datetime(2020, 1, 1, 1, 1)
        responses.add(
            responses.GET,
            "http://foo.com/report/users/42/meetings?user_id=42"
            "&from=1969-01-01T01%3A01%3A00Z&to=2020-01-01T01%3A01%3A00Z",
        )
        self.component.get_user_report(
            user_id="42", start_time=start_time, end_time=end_time
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


if __name__ == "__main__":
    unittest.main()
