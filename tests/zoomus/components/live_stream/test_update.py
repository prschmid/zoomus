from datetime import datetime
import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


class UpdateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.live_stream.LiveStreamComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "patch_request", return_value=True)
    def test_can_update(self, mock_post_request):
        self.component.update(
            meeting_id="42", stream_url="https://foo.bar", stream_key="12345"
        )

        mock_post_request.assert_called_with(
            "/meetings/42/livestream",
            data={
                "meeting_id": "42",
                "stream_url": "https://foo.bar",
                "stream_key": "12345",
            },
        )

    @patch.object(components.base.BaseComponent, "patch_request", return_value=True)
    def test_can_update_wildcard(self, mock_post_request):
        data = {
            "meeting_id": "42",
            "stream_url": "https://foo.bar",
            "stream_key": "12345",
        }
        self.component.update(**data)

        mock_post_request.assert_called_with(
            "/meetings/42/livestream",
            data={
                "meeting_id": "42",
                "stream_url": "https://foo.bar",
                "stream_key": "12345",
            },
        )

    def test_requires_id(self):
        with self.assertRaises(ValueError) as context:
            self.component.update()
            self.assertEqual(context.exception.message, "'meeting_id' must be set")


if __name__ == "__main__":
    unittest.main()
