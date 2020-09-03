import unittest

from zoomus import components
import responses


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

    @responses.activate
    def test_can_get_meeting(self):
        responses.add(responses.GET, "http://foo.com/metrics/meetings/ID?meeting_id=ID")
        self.component.get_meeting(meeting_id="ID")

    @responses.activate
    def test_can_get_participant_qos(self):
        responses.add(
            responses.GET,
            "http://foo.com/metrics/meetings/ID/participants/PID/qos?meeting_id=ID&participant_id=PID",
        )
        self.component.get_participant_qos(meeting_id="ID", participant_id="PID")

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
