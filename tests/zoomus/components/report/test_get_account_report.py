__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

import datetime
import unittest

from mock import patch

from zoomus import (
    components,
    util)


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetAccountReportTestCase))
    return suite


class GetAccountReportTestCase(unittest.TestCase):

    def setUp(self):
        self.component = components.report.ReportComponent(
            base_uri="http://foo.com",
            config={
                'api_key': 'KEY',
                'api_secret': 'SECRET'
            }
        )

    def test_can_get_account_report(self):
        with patch.object(components.base.BaseComponent, 'post_request',
                          return_value=True) as mock_post_request:

            start_time = datetime.datetime.utcnow()
            end_time = datetime.datetime.utcnow()
            self.component.get_account_report(
                start_time=start_time, end_time=end_time)

            mock_post_request.assert_called_with(
                "/report/getaccountreport",
                params={
                    'from': util.date_to_str(start_time),
                    'to': util.date_to_str(end_time)
                }
            )

    def test_requires_start_time(self):
        with self.assertRaises(ValueError) as context:
            self.component.get_account_report()
            self.assertEqual(
                context.exception.message, "'start_time' must be set")

    def test_requires_end_time(self):
        with self.assertRaises(ValueError) as context:
            self.component.get_account_report(start_time=datetime.datetime.utcnow())
            self.assertEqual(
                context.exception.message, "'end_time' must be set")

    def test_does_convert_start_time_to_str_if_datetime(self):

        with patch.object(components.base.BaseComponent, 'post_request',
                          return_value=True) as mock_post_request:

            start_time = datetime.datetime.utcnow()
            end_time = datetime.datetime.utcnow()

            self.component.get_account_report(
                start_time=start_time, end_time=end_time)

            mock_post_request.assert_called_with(
                "/report/getaccountreport",
                params={
                    'from': util.date_to_str(start_time),
                    'to': util.date_to_str(end_time)
                }
            )


if __name__ == '__main__':
    unittest.main()
