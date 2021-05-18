import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeleteRegistrantV2TestCase))
    return suite


class DeleteRegistrantV2TestCase(unittest.TestCase):
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
    def test_can_delete_registrant(self):
        responses.add(
            responses.DELETE,
            "http://foo.com/meetings/ID/registrants/REGISTRANT_ID",
        )
        self.component.delete_registrant(
            id="ID", registrant_id ="REGISTRANT_ID"
        )

    def test_requires_meeting_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.delete_registrant()

    def test_requires_registrant_id(self):
        with self.assertRaisesRegexp(ValueError, "'registrant_id' must be set"):
            self.component.delete_registrant()


if __name__ == "__main__":
    unittest.main()
