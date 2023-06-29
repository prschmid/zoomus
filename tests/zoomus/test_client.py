import unittest

from zoomus import components, ZoomClient, util
from zoomus.client import API_BASE_URIS, OAUTH_URI

try:
    from unittest import mock
except ImportError:
    import mock  # type: ignore


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZoomClientTestCase))
    return suite


class ZoomClientTestCase(unittest.TestCase):

    @mock.patch("zoomus.client.util.generate_token")
    def test_invalid_api_version_raises_error(self, mock_token):
        with self.assertRaisesRegexp(RuntimeError, "API version not supported: 42"):
            ZoomClient("KEY", "SECRET", "ACCOUNT_ID", version=42)

    @mock.patch("zoomus.client.util.generate_token")
    def test_init_sets_config_with_timeout(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID", timeout=500)
        self.assertEqual(client.timeout, 500)

    @mock.patch("zoomus.client.util.generate_token")
    def test_cannot_init_with_non_int_timeout(self, mock_token):
        with self.assertRaises(ValueError) as context:
            ZoomClient("KEY", "SECRET", "ACCOUNT_ID", timeout="bad")
            self.assertEqual(
                context.exception.message, "timeout value must be an integer"
            )

    @mock.patch("zoomus.client.util.generate_token")
    def test_init_creates_all_components(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertEqual(
            set(
                [
                    "contacts",
                    "group",
                    "live_stream",
                    "meeting",
                    "metric",
                    "past_meeting",
                    "phone",
                    "recording",
                    "report",
                    "room",
                    "user",
                    "webinar",
                ]
            ),
            set(client.components.keys()),
        )
        self.assertIsInstance(
            client.components["contacts"], components.contacts.ContactsComponentV2
        )
        self.assertIsInstance(
            client.components["meeting"], components.meeting.MeetingComponentV2
        )
        self.assertIsInstance(
            client.components["metric"], components.metric.MetricComponentV2
        )
        self.assertIsInstance(
            client.components["past_meeting"],
            components.past_meeting.PastMeetingComponentV2,
        )
        self.assertIsInstance(
            client.components["report"], components.report.ReportComponentV2
        )
        self.assertIsInstance(
            client.components["user"], components.user.UserComponentV2
        )
        self.assertIsInstance(
            client.components["webinar"], components.webinar.WebinarComponentV2
        )
        self.assertIsInstance(
            client.components["recording"], components.recording.RecordingComponentV2
        )
        self.assertIsInstance(
            client.components["phone"], components.phone.PhoneComponentV2
        )
        self.assertIsInstance(
            client.components["group"], components.group.GroupComponentV2
        )
        self.assertIsInstance(
            client.components["live_stream"],
            components.live_stream.LiveStreamComponentV2,
        )
        self.assertIsInstance(
            client.components["room"], components.room.RoomComponentV2
        )

    @mock.patch("zoomus.client.util.generate_token")
    def test_api_version_defaults_to_2(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertEqual(client.config["version"], util.API_VERSION_2)
        for key in client.components.keys():
            self.assertEqual(
                client.components[key].base_uri, API_BASE_URIS[util.API_VERSION_2]
            )

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_set_api_version_to_1(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID", version=util.API_VERSION_1)
        self.assertEqual(client.config["version"], util.API_VERSION_1)
        for key in client.components.keys():
            self.assertEqual(
                client.components[key].base_uri, API_BASE_URIS[util.API_VERSION_1]
            )

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_set_base_uri_to_gdpr(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID", base_uri=API_BASE_URIS[util.API_GDPR])
        self.assertEqual(client.config["version"], util.API_VERSION_2)
        for key in client.components.keys():
            self.assertEqual(
                client.components[key].base_uri, API_BASE_URIS[util.API_GDPR]
            )

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_set_custom_base_uri(self, mock_token):
        client = ZoomClient(
            "KEY", "SECRET", "ACCOUNT_ID", version=util.API_VERSION_1, base_uri="https://www.test.com"
        )
        self.assertEqual(client.config["version"], util.API_VERSION_1)
        for key in client.components.keys():
            self.assertEqual(client.components[key].base_uri, "https://www.test.com")

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_set_api_version_to_1_and_set_custom_base_uri(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID", base_uri=API_BASE_URIS[util.API_GDPR])
        self.assertEqual(client.config["version"], util.API_VERSION_2)
        for key in client.components.keys():
            self.assertEqual(
                client.components[key].base_uri, API_BASE_URIS[util.API_GDPR]
            )

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_api_key(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertEqual(client.api_key, "KEY")

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_set_api_key(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        client.api_key = "NEW-KEY"
        self.assertEqual(client.api_key, "NEW-KEY")

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_api_secret(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertEqual(client.api_secret, "SECRET")

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_set_api_secret(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        client.api_secret = "NEW-SECRET"
        self.assertEqual(client.api_secret, "NEW-SECRET")

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_contacts_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(client.contacts, components.contacts.ContactsComponentV2)

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_meeting_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(client.meeting, components.meeting.MeetingComponentV2)

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_report_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(client.report, components.report.ReportComponentV2)

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_user_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(client.user, components.user.UserComponentV2)

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_webinar_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(client.webinar, components.webinar.WebinarComponentV2)

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_recording_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(
            client.recording, components.recording.RecordingComponentV2
        )

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_live_stream_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(
            client.live_stream, components.live_stream.LiveStreamComponentV2
        )

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_phone_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(client.phone, components.phone.PhoneComponentV2)

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_group_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(client.group, components.group.GroupComponentV2)

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_get_room_component(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        self.assertIsInstance(client.room, components.room.RoomComponentV2)

    @mock.patch("zoomus.client.util.generate_token")
    def test_can_use_client_with_context(self, mock_token):
        with ZoomClient("KEY", "SECRET", "ACCOUNT_ID") as client:
            self.assertIsInstance(client, ZoomClient)

    @mock.patch("zoomus.client.util.generate_token")
    def test_refresh_token_replaces_config_token_with_new_token(self, mock_token):
        client = ZoomClient("KEY", "SECRET", "ACCOUNT_ID")
        client.refresh_token()
        mock_token.assert_called_with(OAUTH_URI, "KEY", "SECRET", "ACCOUNT_ID")
        self.assertEqual(client.config["token"], (mock_token.return_value,))


if __name__ == "__main__":
    unittest.main()
