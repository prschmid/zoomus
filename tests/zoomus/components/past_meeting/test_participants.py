import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ParticipantsV2TestCase))
    return suite


class ParticipantsV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.past_meeting.PastMeetingComponentV2(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )

    @responses.activate
    def test_can_list(self):
        responses.add(
            responses.GET, "http://www.foo.com/past_meetings/ID/participants",
        )
        self.component.get_participants(meeting_id="ID")
        expected_headers = {"Authorization": "Bearer token"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    def test_requires_user_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.get_participants()


if __name__ == "__main__":
    unittest.main()
