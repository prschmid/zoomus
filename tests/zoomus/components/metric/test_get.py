import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetMetricV2TestCase))
    return suite


class GetMetricV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.metric.MetricComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_get_meeting(self, mock_get_request):
        self.component.get_meeting(meeting_id="ID")
        mock_get_request.assert_called_with(
            "/metrics/meetings/ID", params={"meeting_id": "ID"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_get_participant_qos(self, mock_get_request):
        self.component.get_participant_qos(meeting_id="ID", participant_id="PID")
        mock_get_request.assert_called_with(
            "/metrics/meetings/ID/participants/PID/qos",
            params={"meeting_id": "ID", "participant_id": "PID"},
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.get_meeting()

    def test_get_participant_qos_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.get_participant_qos(participant_id="PID")

    def test_get_participant_qos_requires_participant_id(self):
        with self.assertRaisesRegexp(ValueError, "'participant_id' must be set"):
            self.component.get_participant_qos(meeting_id="PID")


if __name__ == "__main__":
    unittest.main()
