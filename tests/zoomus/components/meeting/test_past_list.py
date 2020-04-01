import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


class PastListV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_list(self, mock_get_request):
        self.component.list(meeting_id="ID")

        mock_get_request.assert_called_with(
            "/past_meetings/ID/instances", params={"meeting_id": "ID"}
        )

    def test_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.list()


if __name__ == "__main__":
    unittest.main()
