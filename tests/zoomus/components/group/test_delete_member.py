import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeleteV1TestCase))
    suite.addTest(unittest.makeSuite(DeleteV2TestCase))
    return suite


class DeleteMemberV2TestCase(unittest.TestCase):
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
    def test_can_delete(self):
        responses.add(responses.DELETE, "http://foo.com/groups/42/members/13")
        self.component.delete_member(groupid="42", memberid="13")

    def test_requires_groupid(self):
        with self.assertRaisesRegexp(ValueError, "'groupid' must be set"):
            self.component.delete_member()

    def test_requires_memberid(self):
        with self.assertRaisesRegexp(ValueError, "'memberid' must be set"):
            self.component.delete_member(groupid="foo")


if __name__ == "__main__":
    unittest.main()
