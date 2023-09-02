import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateV1TestCase))
    suite.addTest(unittest.makeSuite(CreateV2TestCase))
    return suite


class AddMemberV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.group.GroupComponentV2(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_add_members(self):
        responses.add(responses.POST, "http://foo.com/groups/ID/members")
        response = self.component.add_members(
            groupid="ID", members=["test1@example.com", "test2@example.com"]
        )

    def test_requires_groupid(self):
        with self.assertRaisesRegexp(ValueError, "'groupid' must be set"):
            self.component.add_members()

    def test_requires_members(self):
        with self.assertRaisesRegexp(ValueError, "'members' must be set"):
            self.component.add_members(groupid="foo")
