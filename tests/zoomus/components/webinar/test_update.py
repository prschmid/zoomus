from datetime import datetime
import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateV1TestCase))
    return suite


class UpdateV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "post_request", return_value=True)
    def test_can_update(self, mock_post_request):
        self.component.update(id="ID", host_id="ID")

        mock_post_request.assert_called_with(
            "/webinar/update", params={"id": "ID", "host_id": "ID"}
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update()

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.update(id="ID")

    @patch.object(components.base.BaseComponent, "post_request", return_value=True)
    def test_start_time_gets_transformed(self, mock_post_request):
        self.component.update(id="42", host_id="HOST", start_time=datetime(1969, 1, 1))
        mock_post_request.assert_called_with(
            "/webinar/update",
            params={
                "id": "42",
                "host_id": "HOST",
                "start_time": "1969-01-01T00:00:00Z",
            },
        )


class UpdateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "patch_request", return_value=True)
    def test_can_update(self, mock_patch_request):
        self.component.update(id="ID")

        mock_patch_request.assert_called_with("/webinars/ID", params={"id": "ID"})

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update()


if __name__ == "__main__":
    unittest.main()
