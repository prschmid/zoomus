import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetV2TestCase))
    return suite


class GetV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.past_meeting.PastMeetingComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @responses.activate
    def test_can_get(self):
        responses.add(responses.GET, "http://foo.com/past_meetings/ID?meeting_id=ID")
        self.component.get(meeting_id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.get()


if __name__ == "__main__":
    unittest.main()
