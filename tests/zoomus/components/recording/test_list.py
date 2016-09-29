__author__ = "Tomas Garzon"
__email__ = "tomasgarzonhervas@gmail.com"

import datetime
import unittest

from mock import patch

from zoomus import (
    components,
    util)


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ListTestCase))
    return suite


class ListTestCase(unittest.TestCase):

    def setUp(self):
        self.component = components.recording.RecordingComponent(
            base_uri="http://foo.com",
            config={
                'api_key': 'KEY',
                'api_secret': 'SECRET'
            }
        )

    def test_can_list(self):
        with patch.object(components.base.BaseComponent, 'post_request',
                          return_value=True) as mock_post_request:

            self.component.list(host_id='ID')

            mock_post_request.assert_called_with(
                "/recording/list",
                params={
                    'host_id': 'ID'
                }
            )

    def test_requires_host_id(self):
        with self.assertRaises(ValueError) as context:
            self.component.list()
            self.assertEqual(
                context.exception.message, "'host_id' must be set")

    def test_does_convert_startime_to_str_if_datetime(self):

        with patch.object(components.base.BaseComponent, 'post_request',
                          return_value=True) as mock_post_request:

            start_time = datetime.datetime.utcnow() - datetime.timedelta(days=10)
            end_time = datetime.datetime.utcnow()
            self.component.list(
                host_id='ID',
                start=start_time,
                end=end_time,
                meeting_number="111")

            mock_post_request.assert_called_with(
                "/recording/list",
                params={
                    'host_id': 'ID',
                    'from': util.date_to_str(start_time),
                    'to': util.date_to_str(end_time),
                    "meeting_number": "111"
                }
            )


if __name__ == '__main__':
    unittest.main()
