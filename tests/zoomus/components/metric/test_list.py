import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ListV2TestCase))
    return suite


class ListV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.metric.MetricComponentV2(
            base_uri="http://foo.com", config={"client_id": "CLIENT_ID", "client_secret": "SECRET"}
        )

    @responses.activate
    def test_can_list(self):
        responses.add(responses.GET, "http://foo.com/metrics/meetings")
        self.component.list_meetings()

    @responses.activate
    def test_can_list_participants(self):
        responses.add(
            responses.GET,
            "http://foo.com/metrics/meetings/ID/participants?meeting_id=ID",
        )
        self.component.list_participants(meeting_id="ID")

    @responses.activate
    def test_can_list_participants_qos(self):
        responses.add(
            responses.GET,
            "http://foo.com/metrics/meetings/ID/participants/qos?meeting_id=ID",
        )
        self.component.list_participants_qos(meeting_id="ID")

    def test_list_participants_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.list_participants()

    def test_list_participants_qos_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.list_participants_qos()


if __name__ == "__main__":
    unittest.main()
