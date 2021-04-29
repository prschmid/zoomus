import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AddRegistrantV2TestCase))
    return suite


class AddRegistrantV2TestCase(unittest.TestCase):
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
    def test_can_add_registrant(self):
        responses.add(
            responses.POST,
            "http://foo.com/meetings/ID/registrants",
        )
        response = self.component.add_registrant(
            id="ID", email="EMAIL", last_name="LAST_NAME", first_name="FIRST_NAME"
        )
        self.assertEqual(
            response.request.body,
            '{"id": "ID", "email": "EMAIL", "last_name": "LAST_NAME", "first_name": "FIRST_NAME"}',
        )

    def test_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.add_registrant()


if __name__ == "__main__":
    unittest.main()
