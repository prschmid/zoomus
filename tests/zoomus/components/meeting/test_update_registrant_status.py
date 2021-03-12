import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateRegistrantStatusV2TestCase))
    return suite


class UpdateRegistrantStatusV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_update_registrant(self):
        responses.add(
            responses.PUT, "http://foo.com/meetings/ID/registrants/status",
        )
        response = self.component.update_registrant_status(id="ID", action="approve", registrants=[{'email':"EMAIL"}])
        self.assertEqual(responses.calls[0].request.body, '{"id": "ID", "action": "approve", "registrants": [{"email": "EMAIL"}]}')

    def test_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update_registrant_status()

    def test_requires_action(self):
        with self.assertRaisesRegexp(ValueError, "'action' must be set"):
            self.component.update_registrant_status(id="ID")

    def test_requires_registrants(self):
        with self.assertRaisesRegexp(ValueError, "'registrants' must be set"):
            self.component.update_registrant_status(id="ID", action="approve")


if __name__ == "__main__":
    unittest.main()
