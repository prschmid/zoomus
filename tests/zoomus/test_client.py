import unittest

from zoomus import (
    components,
    ZoomClient,
    util)


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZoomClientTestCase))
    return suite


class ZoomClientTestCase(unittest.TestCase):

    def test_init_sets_config(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertEqual(
            client.config,
            {
                'api_key': 'KEY',
                'api_secret': 'SECRET',
                'data_type': 'json',
                'token': util.generate_jwt('KEY', 'SECRET'),
                'version': 1,
            }
        )

    def test_init_sets_config_with_timeout(self):
        client = ZoomClient('KEY', 'SECRET', timeout=500)
        self.assertEqual(client.timeout, 500)

    def test_cannot_init_with_non_int_timeout(self):
        with self.assertRaises(ValueError) as context:
            ZoomClient('KEY', 'SECRET', timeout='bad')
            self.assertEqual(
                context.exception.message, "timeout value must be an integer")

    def test_init_creates_all_components(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertEqual(
            set(['meeting', 'report', 'user', 'webinar', 'recording']),
            set(client.components.keys())
        )
        self.assertIsInstance(
            client.components['meeting'],
            components.meeting.MeetingComponent
        )
        self.assertIsInstance(
            client.components['report'],
            components.report.ReportComponent
        )
        self.assertIsInstance(
            client.components['user'],
            components.user.UserComponent
        )
        self.assertIsInstance(
            client.components['webinar'],
            components.webinar.WebinarComponent
        )
        self.assertIsInstance(
            client.components['recording'],
            components.recording.RecordingComponent
        )

    def test_can_get_api_key(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertEqual(client.api_key, 'KEY')

    def test_can_set_api_key(self):
        client = ZoomClient('KEY', 'SECRET')
        client.api_key = 'NEW-KEY'
        self.assertEqual(client.api_key, 'NEW-KEY')

    def test_can_get_api_secret(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertEqual(client.api_secret, 'SECRET')

    def test_can_set_api_secret(self):
        client = ZoomClient('KEY', 'SECRET')
        client.api_secret = 'NEW-SECRET'
        self.assertEqual(client.api_secret, 'NEW-SECRET')

    def test_can_get_meeting_component(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertIsInstance(
            client.meeting,
            components.meeting.MeetingComponent
        )

    def test_can_get_report_component(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertIsInstance(
            client.report,
            components.report.ReportComponent
        )

    def test_can_get_user_component(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertIsInstance(
            client.user,
            components.user.UserComponent
        )

    def test_can_get_webinar_component(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertIsInstance(
            client.webinar,
            components.webinar.WebinarComponent
        )

    def test_can_get_recording_component(self):
        client = ZoomClient('KEY', 'SECRET')
        self.assertIsInstance(
            client.recording,
            components.recording.RecordingComponent
        )

    def test_can_use_client_with_context(self):
        with ZoomClient('KEY', 'SECRET') as client:
            self.assertIsInstance(
                client,
                ZoomClient
            )


if __name__ == '__main__':
    unittest.main()
