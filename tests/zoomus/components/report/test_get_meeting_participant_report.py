import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetMeetingParticipantReportV2TestCase))
    return suite


class GetMeetingParticipantReportV2TestCase(unittest.TestCase):
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
    def test_can_get_meeting_participant_report(self):
        responses.add(
            responses.GET,
            "http://foo.com/report/meetings/42/participants?meeting_id=42",
        )
        self.component.get_meeting_participant_report(meeting_id="42")

    @responses.activate
    def test_encode_meeting_id(self):
        responses.add(
            responses.GET,
            "http://foo.com/report/meetings/%252Fsomeidwith%252F%252Fslashes/participants?meeting_id=%25252Fsomeidwith%25252F%25252Fslashes",
        )
        self.component.get_meeting_participant_report(meeting_id="/someidwith//slashes")

    def test_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.get_meeting_participant_report()


if __name__ == "__main__":
    unittest.main()
