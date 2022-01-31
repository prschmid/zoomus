import unittest
from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(GetV1TestCase))
    suite.addTest(unittest.makeSuite(InviteTextV2TestCase))
    return suite


class InviteTextV2TestCase(unittest.TestCase):
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
    def test_invite_text(self):
        responses.add(
            responses.GET,
            "http://foo.com/meetings/ID/invitation",
        )
        self.component.invite_text(id="ID")
        assert responses.assert_call_count("http://foo.com/meetings/ID/invitation", 1)

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.invite_text()
