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
    suite.addTest(unittest.makeSuite(ListV2TestCase))
    return suite


class ListV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.metric.MetricComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_list(self, mock_get_request):
        self.component.list_meetings()

        mock_get_request.assert_called_with("/metrics/meetings", params={})

    def test_list_participants_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.list_participants()


if __name__ == "__main__":
    unittest.main()
